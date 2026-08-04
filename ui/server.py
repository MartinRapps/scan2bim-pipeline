#!/usr/bin/env python3
"""
Pipeline Status Dashboard Server
Serves the UI and API endpoints for the Scan-to-BIM pipeline.
"""
import os
import csv
import json
import math
import mimetypes
import pty
import select
import subprocess
import tempfile
import threading
import queue
import uuid
import signal
from http.server import HTTPServer, SimpleHTTPRequestHandler
from socketserver import ThreadingMixIn
from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse, parse_qs, quote, unquote

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
PUBLIC_DIR = os.path.join(os.path.dirname(__file__), 'public')
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# GCP registration paths (used by the /api/gcp/* endpoints).
SFM_DIR = os.path.join(DATA_DIR, "04_sfm")
SPARSE_TXT_DIR = os.path.join(SFM_DIR, "sparse_txt")
GCP_OBS_PATH = os.path.join(SFM_DIR, "gcp_observations.json")
GCP_REPORT_PATH = os.path.join(SFM_DIR, "gcp_report.json")
RAW_DIR = os.path.join(DATA_DIR, "01_raw")
GCP_RELATIVE_CSV = os.path.join(RAW_DIR, "gcp_relative.csv")
GCP_COORDINATES_CSV = os.path.join(RAW_DIR, "gcp_coordinates.csv")
FRAMES_DIR = os.path.join(DATA_DIR, "02_frames")
GCP_OBS_LOCK = threading.Lock()


def _quat_to_rotmat(q):
    qw, qx, qy, qz = q
    return [
        [1 - 2 * (qy * qy + qz * qz), 2 * (qx * qy - qz * qw), 2 * (qx * qz + qy * qw)],
        [2 * (qx * qy + qz * qw), 1 - 2 * (qx * qx + qz * qz), 2 * (qy * qz - qx * qw)],
        [2 * (qx * qz - qy * qw), 2 * (qy * qz + qx * qw), 1 - 2 * (qx * qx + qy * qy)],
    ]


def _camera_center(qvec, tvec):
    """World-space camera center C = -R^T @ t (pure python, no numpy)."""
    R = _quat_to_rotmat(qvec)
    Rt_t = [sum(R[r][c] * tvec[r] for r in range(3)) for c in range(3)]  # R^T @ t
    return [-x for x in Rt_t]


def _parse_cameras_txt_min(path):
    cams = {}
    try:
        with open(path, encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                parts = line.split()
                cams[int(parts[0])] = {"model": parts[1], "width": int(parts[2]), "height": int(parts[3])}
    except OSError:
        pass
    return cams


def _parse_images_txt_min(path):
    images = []
    try:
        with open(path, encoding="utf-8") as handle:
            lines = [line.rstrip("\n") for line in handle if not line.lstrip().startswith("#")]
    except OSError:
        return images
    for i in range(0, len(lines), 2):
        parts = lines[i].split()
        if not parts:
            continue
        images.append({
            "name": parts[9],
            "camera_id": int(parts[8]),
            "qvec": [float(x) for x in parts[1:5]],
            "tvec": [float(x) for x in parts[5:8]],
        })
    return images


def _parse_gcp_csv(path):
    """Return {gcp_id: [x, y, z]} from a GCP coordinate CSV (id + x/y/z columns)."""
    points = {}
    if not os.path.isfile(path):
        return points
    try:
        with open(path, encoding="utf-8") as handle:
            reader = csv.reader(handle)
            header = [h.strip() for h in next(reader)]
            lower = [h.lower() for h in header]
            id_idx = next((i for i, c in enumerate(lower) if c in ("id", "name", "gcp", "passpunkt", "gcp_id")), None)
            x_idx = next((i for i, c in enumerate(lower) if c in ("x", "east", "ost", "easting")), None)
            y_idx = next((i for i, c in enumerate(lower) if c in ("y", "north", "nord", "northing")), None)
            z_idx = next((i for i, c in enumerate(lower) if c in ("z", "height", "hoehe", "elevation")), None)
            if None in (id_idx, x_idx, y_idx, z_idx):
                return points
            for row in reader:
                if not row:
                    continue
                points[row[id_idx].strip()] = [float(row[x_idx]), float(row[y_idx]), float(row[z_idx])]
    except (OSError, ValueError, StopIteration):
        pass
    return points


def _read_observations():
    if not os.path.isfile(GCP_OBS_PATH):
        return []
    try:
        with open(GCP_OBS_PATH, encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, ValueError):
        return []


def _write_observations(observations):
    os.makedirs(os.path.dirname(GCP_OBS_PATH), exist_ok=True)
    temporary_path = f"{GCP_OBS_PATH}.tmp"
    try:
        with open(temporary_path, "w", encoding="utf-8") as handle:
            json.dump(observations, handle, indent=2)
            handle.write("\n")
        os.replace(temporary_path, GCP_OBS_PATH)
    finally:
        try:
            os.unlink(temporary_path)
        except FileNotFoundError:
            pass


def _invalidate_gcp_registration():
    """Remove derived registration outputs after observations change."""
    for path in (GCP_REPORT_PATH, os.path.join(SFM_DIR, "matrix.txt")):
        try:
            os.unlink(path)
        except FileNotFoundError:
            pass


def safe_write(self, data):
    """Write data to the response stream; return True on success, False if the
    client has disconnected. Callers that replay cached state must stop once
    this returns False so they do not silently truncate the replay."""
    try:
        if isinstance(data, str):
            data = data.encode()
        self.wfile.write(data)
        self.wfile.flush()
        return True
    except (ConnectionResetError, BrokenPipeError, OSError):
        return False


def safe_send_json(self, data, status=200):
    try:
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode())
    except (ConnectionResetError, BrokenPipeError, OSError):
        pass


SCRIPTS_INFO = [
    {
        "id": "run_pipeline",
        "name": "run_pipeline.sh",
        "args": [],
        "description": "F\u00fchrt die gesamte Scan-to-BIM Pipeline von der GCP-Vorbereitung bis zum GIS-Export aus. Inkludiert SAM 3.1 Segmentierung, COLMAP SfM, STS 3DGS Training, SuGaR Meshing und Post-Processing.",
        "steps": [
            "GCP-Vorbereitung",
            "SAM 3.1 Tracking & Masken",
            "COLMAP SfM",
            "GCP-Registrierung (UI / CloudCompare Breakpoint)",
            "STS 3DGS Training",
            "SuGaR Meshing",
            "DGtal Centerline",
            "GIS-Export",
        ],
        "inputs": [
            {"prompt": "HuggingFace Token f\u00fcr SAM 3.1", "var": "HF_TOKEN", "type": "password"},
            {"prompt": "Text-Prompt (z.B. 'cable', 'pipe')", "var": "TEXT_PROMPT"},
            {"prompt": "Video verwenden / komprimieren", "var": "VIDEO_CONFIG", "type": "confirm"},
            {"prompt": "STS Gesamtiterationen (Objektphase + All-Object-Phase)", "var": "ITERATIONS", "default": "7000"},
            {"prompt": "Objekt-/Stage-2-Iterationen", "var": "STAGE2_ITERS", "default": "5000"},
            {"prompt": "On-the-fly GPU-Modus", "var": "ON_THE_FLY", "type": "confirm"},
        ],
    },
    {
        "id": "run_from_colmap",
        "name": "run_pipeline.sh",
        "args": ["--from", "colmap"],
        "description": "Replay ab COLMAP SfM (run_pipeline.sh --from colmap). \u00dcberspringt die SAM 3.1 Maskengenerierung. N\u00fctzlich wenn die Masken bereits vorhanden sind und nur die 3D-Rekonstruktion wiederholt wird.",
        "steps": [
            "COLMAP SfM",
            "GCP-Registrierung (UI / CloudCompare Breakpoint)",
            "STS Workspace Setup",
            "STS 3DGS Training",
            "Punktwolken-Filterung",
            "SuGaR Meshing",
            "DGtal Centerline",
            "GIS-Export",
        ],
        "inputs": [
            {"prompt": "Autopilot-Modus (y/n)", "var": "AUTOPILOT", "type": "confirm"},
            {"prompt": "STS Gesamtiterationen (Objektphase + All-Object-Phase)", "var": "ITERATIONS", "default": "7000"},
        ],
    },
    {
        "id": "run_from_sts",
        "name": "run_pipeline.sh",
        "args": ["--from", "sts"],
        "description": "Replay ab STS-Training (run_pipeline.sh --from sts). \u00dcberspringt SAM 3.1 und COLMAP, startet direkt bei der 3DGS-Rekonstruktion. N\u00fctzlich wenn Masken und SfM bereits vorhanden sind.",
        "steps": [
            "STS Workspace Setup",
            "STS 3DGS Training",
            "Punktwolken-Filterung",
            "SuGaR Meshing",
            "DGtal Centerline",
            "GIS-Export",
        ],
        "inputs": [
            {"prompt": "Autopilot-Modus (y/n)", "var": "AUTOPILOT", "type": "confirm"},
            {"prompt": "STS Gesamtiterationen (Objektphase + All-Object-Phase)", "var": "ITERATIONS", "default": "7000"},
            {"prompt": "Objekt-/Stage-2-Iterationen", "var": "STAGE2_ITERS", "default": "5000"},
            {"prompt": "On-the-fly GPU-Modus", "var": "ON_THE_FLY", "type": "confirm"},
            {"prompt": "Regularisierung (dn_consistency/density/sdf oder EXPLAIN)", "var": "REGULARIZATION"},
            {"prompt": "Refinement-Dauer (short/medium/long oder EXPLAIN)", "var": "REFINEMENT_TIME"},
        ],
    },
    {
        "id": "run_from_sugar",
        "name": "run_pipeline.sh",
        "args": ["--from", "sugar"],
        "description": "Replay ab SuGaR-Meshing (run_pipeline.sh --from sugar). Ben\u00f6tigt einen fertigen STS-Checkpoint. Ideal zum schnellen Testen des Meshing- und Post-Processing-Schritts.",
        "steps": [
            "SuGaR Coarse-Training + Meshing + Refinement",
            "DGtal Centerline",
            "GIS-Export",
        ],
        "inputs": [
            {"prompt": "Autopilot-Modus (y/n)", "var": "AUTOPILOT", "type": "confirm"},
            {"prompt": "Checkpoint-Iteration (bestehender Replay-Default)", "var": "ITERATIONS", "default": "7000"},
            {"prompt": "Regularisierung (dn_consistency/density/sdf oder EXPLAIN)", "var": "REGULARIZATION"},
            {"prompt": "Refinement-Dauer (short/medium/long oder EXPLAIN)", "var": "REFINEMENT_TIME"},
        ],
    },
]

# Script execution sessions
script_sessions = {}
script_sessions_lock = threading.Lock()


def run_script_thread(script_path, session_id, script_args=None):
    """Run a shell script inside a pseudo-terminal (PTY).

    A PTY (instead of plain pipes) is essential for interactive scripts:
    'read -p' prompts are written without a trailing newline and bash also
    detects a TTY, so prompts are flushed immediately and appear live in the
    browser terminal. It also lets us forward user answers to stdin.
    ``script_args`` is forwarded as argv after the script path (e.g. for
    ``run_pipeline.sh --from sts``).
    """
    q = script_sessions[session_id]["queue"]
    proc = None
    master_fd = None
    script_args = script_args or []
    try:
        master_fd, slave_fd = pty.openpty()
        proc = subprocess.Popen(
            ["/bin/bash", script_path, *script_args],
            stdin=slave_fd,
            stdout=slave_fd,
            stderr=slave_fd,
            cwd=PROJECT_ROOT,
            close_fds=True,
            preexec_fn=os.setsid,  # own process group -> we can kill children (docker compose run) too
            env={**os.environ, "TERM": "dumb", "PYTHONUNBUFFERED": "1"},
        )
        os.close(slave_fd)
        with script_sessions_lock:
            script_sessions[session_id]["process"] = proc
            script_sessions[session_id]["master_fd"] = master_fd

        while True:
            with script_sessions_lock:
                cancelled = script_sessions.get(session_id, {}).get("cancel")
            if cancelled:
                try:
                    os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
                except (ProcessLookupError, OSError):
                    pass
                break
            rlist, _, _ = select.select([master_fd], [], [], 0.5)
            if rlist:
                try:
                    data = os.read(master_fd, 8192)
                except OSError:
                    break  # PTY closed (process exited)
                if not data:
                    break
                clean_text = data.decode("utf-8", errors="replace")
                with script_sessions_lock:
                    if session_id in script_sessions:
                        script_sessions[session_id]["log"].append(clean_text)
                q.put(("output", clean_text))
            elif proc.poll() is not None:
                break
        proc.wait()
        q.put(("exit", proc.returncode))
    except Exception as e:
        err_msg = f"\n[FEHLER] {e}\n"
        with script_sessions_lock:
            if session_id in script_sessions:
                script_sessions[session_id]["log"].append(err_msg)
        q.put(("output", err_msg))
        q.put(("exit", -1))
    finally:
        if master_fd is not None:
            try:
                os.close(master_fd)
            except OSError:
                pass
        with script_sessions_lock:
            if session_id in script_sessions:
                script_sessions[session_id]["process"] = None
                script_sessions[session_id]["master_fd"] = None


def handle_script_serve(handler, session_id):
    with script_sessions_lock:
        session = script_sessions.get(session_id)
    if not session:
        handler.send_json({"error": "Session not found"}, 404)
        return
    try:
        handler.send_response(200)
        handler.send_header("Content-Type", "text/event-stream")
        handler.send_header("Cache-Control", "no-cache")
        handler.send_header("Connection", "keep-alive")
        handler.send_header("Access-Control-Allow-Origin", "*")
        handler.end_headers()
    except (ConnectionResetError, BrokenPipeError, OSError):
        return

    # First stream any cached historical terminal outputs (allows restoring state on refresh!)
    with script_sessions_lock:
        historical_logs = list(session.get("log", []))
    for log_item in historical_logs:
        payload = json.dumps({"type": "output", "data": log_item})
        if not safe_write(handler, f"data: {payload}\n\n"):
            return

    q = session["queue"]
    while True:
        try:
            msg_type, data = q.get(timeout=2)
            payload = json.dumps({"type": msg_type, "data": data})
            safe_write(handler, f"data: {payload}\n\n")
            if msg_type == "exit":
                break
        except queue.Empty:
            safe_write(handler, "data: {\"type\":\"heartbeat\"}\n\n")
    cleanup_script_session(session_id)


def cleanup_script_session(session_id):
    with script_sessions_lock:
        if session_id in script_sessions:
            proc = script_sessions[session_id].get("process")
            if proc:
                try:
                    os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
                except (ProcessLookupError, OSError):
                    try:
                        proc.terminate()
                    except Exception:
                        pass
            del script_sessions[session_id]


def send_script_input(session_id, text):
    """Forward user input from the browser to the script's PTY (stdin)."""
    with script_sessions_lock:
        session = script_sessions.get(session_id)
        if not session:
            return False
        proc = session.get("process")
        master_fd = session.get("master_fd")
    if proc and master_fd is not None and proc.poll() is None:
        try:
            os.write(master_fd, (text + "\n").encode())
            return True
        except OSError:
            return False
    return False


PIPELINE_STEPS = [
    {
        "id": "raw",
        "label": "01 Rohdaten (Video/GNSS)",
        "dir": "01_raw",
        "container": "Host",
        "scripts": ["run_pipeline.sh", "prepare_gcp.py"],
        "outputs": ["*.mp4", "*.mov", "*.jpg"],
    },
    {
        "id": "frames",
        "label": "02 Frame-Extraktion",
        "dir": "02_frames",
        "container": "Container A (SAM 3)",
        "scripts": ["extract_masks_notebook_flow.py"],
        "outputs": ["*.jpg", "*.png"],
    },
    {
        "id": "masks",
        "label": "03 SAM 3 Masken",
        "dir": "03_masks",
        "container": "Container A (SAM 3)",
        "scripts": ["extract_masks_notebook_flow.py"],
        "outputs": ["*mask*.png", "*_obj_*.png"],
    },
    {
        "id": "sfm",
        "label": "04 COLMAP SfM",
        "dir": "04_sfm",
        "container": "Container B (COLMAP)",
        "scripts": ["run_sfm.sh"],
        "outputs": ["points3D.ply", "database.db", "sparse/"],
    },
    {
        "id": "sts",
        "label": "05 STS 3DGS Training",
        "dir": "05_3dgs",
        "container": "Container C (STS)",
        "scripts": ["prep_sts_scene.py", "filter_cable_pc.py"],
        "outputs": ["output/point_cloud/*.ply", "output/*.pth"],
    },
    {
        "id": "mesh",
        "label": "06 SuGaR Meshing",
        "dir": "06_mesh",
        "container": "Container D (SuGaR)",
        "scripts": ["run_masked_sugar.sh", "prepare_sugar_input.sh"],
        "outputs": ["*.ply", "*.obj"],
    },
    {
        "id": "centerline",
        "label": "07 DGtal Centerline",
        "dir": "07_centerline",
        "container": "Container E (Post-Processing)",
        "scripts": ["postprocess.sh", "centerline_bspline.py"],
        "outputs": ["*.csv", "*.ply"],
    },
    {
        "id": "gis",
        "label": "08 GIS-Export",
        "dir": "08_gis",
        "container": "Container E (Post-Processing)",
        "scripts": ["postprocess.sh", "transform_centerline.py"],
        "outputs": ["*.geojson", "*.csv", "*.shp"],
    },
    {
        "id": "eval",
        "label": "09 Evaluation",
        "dir": "09_evaluation",
        "container": "Host",
        "scripts": [],
        "outputs": ["*.json", "*.csv", "*.png", "*.pdf"],
    },
]


def scan_dir(dirpath, patterns=None):
    if not os.path.isdir(dirpath):
        return []
    entries = []
    for fname in sorted(os.listdir(dirpath)):
        fpath = os.path.join(dirpath, fname)
        rel = os.path.relpath(fpath, os.path.dirname(DATA_DIR))
        if os.path.islink(fpath) and not os.path.exists(fpath):
            continue
        try:
            stat = os.stat(fpath)
        except (FileNotFoundError, OSError):
            continue
        is_dir = os.path.isdir(fpath) and not os.path.islink(fpath)
        size = stat.st_size if not is_dir else 0
        mtime = datetime.fromtimestamp(stat.st_mtime).isoformat()
        entry = {
            "name": fname,
            "path": rel,
            "size": size,
            "mtime": mtime,
            "is_dir": is_dir,
        }
        if is_dir:
            children = scan_dir(fpath)
            if children:
                entry["children"] = children
        entries.append(entry)
    return entries


def get_step_info(step):
    dirpath = os.path.join(DATA_DIR, step["dir"])
    exists = os.path.isdir(dirpath)
    files = scan_dir(dirpath) if exists else []
    nonempty = len(files) > 0

    ply_files = []
    img_files = []
    video_files = []
    obj_files = []
    pth_files = []
    csv_files = []
    json_files = []
    geojson_files = []

    def collect(fs):
        for f in fs:
            if f.get("children"):
                collect(f["children"])
            name = f["name"].lower()
            if name.endswith(".ply"):
                ply_files.append(f)
            elif name.endswith((".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp")):
                img_files.append(f)
            elif name.endswith((".mp4", ".mov", ".avi", ".webm")):
                video_files.append(f)
            elif name.endswith(".obj"):
                obj_files.append(f)
            elif name.endswith(".pth"):
                pth_files.append(f)
            elif name.endswith(".csv"):
                csv_files.append(f)
            elif name.endswith(".json"):
                json_files.append(f)
            elif name.endswith(".geojson"):
                geojson_files.append(f)

    collect(files)

    preview = {}
    if img_files:
        preview["images"] = img_files[:min(len(img_files), 6)]
    if video_files:
        preview["video"] = video_files[0]
    if ply_files:
        preview["ply"] = ply_files[0]
    if obj_files:
        preview["obj"] = obj_files[0]
    if pth_files:
        preview["checkpoints"] = [f for f in pth_files]
    if csv_files:
        preview["csv"] = csv_files[0]
    if geojson_files:
        preview["geojson"] = geojson_files[0]
    if json_files:
        preview["json"] = json_files[-1] if len(json_files) > 1 else json_files[0]

    return {
        "id": step["id"],
        "label": step["label"],
        "dir": step["dir"],
        "container": step["container"],
        "scripts": step["scripts"],
        "exists": exists,
        "nonempty": nonempty,
        "file_count": len(files) if exists else 0,
        "files": files if nonempty else [],
        "preview": preview,
        "total_file_count": sum(1 for _ in walk_files(dirpath)) if exists else 0,
    }


def walk_files(dirpath):
    for root, dirs, files in os.walk(dirpath):
        for f in files:
            yield os.path.join(root, f)


class DashboardHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=PUBLIC_DIR, **kwargs)

    def do_GET(self):
        if self.path == "/api/steps":
            self.send_json([get_step_info(s) for s in PIPELINE_STEPS])
        elif self.path == "/api/scripts":
            self.send_json(SCRIPTS_INFO)
        elif self.path == "/api/script/active":
            # Return active sessions to allow any client reload to seamlessly reconnect!
            active_list = []
            with script_sessions_lock:
                for sid, s in script_sessions.items():
                    proc = s.get("process")
                    running = proc is not None and proc.poll() is None
                    if running:
                        active_list.append({
                            "session_id": sid,
                            "script_id": s["script_id"]
                        })
            self.send_json(active_list)
        elif self.path.startswith("/api/script/stream/"):
            session_id = self.path.split("/")[-1]
            handle_script_serve(self, session_id)
        elif self.path.startswith("/api/script/status/"):
            session_id = self.path.split("/")[-1]
            with script_sessions_lock:
                session = script_sessions.get(session_id)
            if session:
                proc = session.get("process")
                running = proc is not None and proc.poll() is None
                self.send_json({"running": running, "session_id": session_id})
            else:
                self.send_json({"running": False, "session_id": session_id})
        elif self.path.startswith("/api/file/"):
            rel_path = unquote(self.path[len("/api/file/"):])
            abs_path = os.path.abspath(os.path.join(DATA_DIR, "..", rel_path))
            # Confinement: never serve files outside the project root (blocks
            # /api/file/../../etc/passwd style traversal from the URL).
            if abs_path != PROJECT_ROOT and not abs_path.startswith(PROJECT_ROOT + os.sep):
                self.send_json({"error": "Forbidden"}, 403)
                return
            if os.path.isfile(abs_path):
                try:
                    self.send_response(200)
                    mime, _ = mimetypes.guess_type(abs_path)
                    self.send_header("Content-Type", mime or "application/octet-stream")
                    self.send_header("Content-Length", os.path.getsize(abs_path))
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.end_headers()
                    with open(abs_path, "rb") as f:
                        safe_write(self, f.read())
                except (ConnectionResetError, BrokenPipeError, OSError):
                    pass
            else:
                self.send_json({"error": "File not found"}, 404)
        elif self.path.startswith("/api/dir/"):
            rel_path = unquote(self.path[len("/api/dir/"):])
            abs_path = os.path.abspath(os.path.join(DATA_DIR, rel_path))
            # Confinement: restrict directory listings to the data directory.
            if abs_path != DATA_DIR and not abs_path.startswith(DATA_DIR + os.sep):
                self.send_json({"error": "Forbidden"}, 403)
                return
            if os.path.isdir(abs_path):
                self.send_json(scan_dir(abs_path))
            else:
                self.send_json({"error": "Directory not found"}, 404)
        elif self.path == "/api/info":
            self.send_json({
                "project": "KI-gestützte 3D-Rekonstruktion linearer Infrastruktur",
                "pipeline": "Scan-to-BIM mit SAM 3 + Gaussian Splatting",
                "data_dir": DATA_DIR,
            })
        elif self.path == "/api/gcp/frames":
            self.send_json(self._gcp_frames())
        elif self.path == "/api/gcp/points":
            self.send_json(self._gcp_points())
        elif self.path == "/api/gcp/observations":
            self.send_json(_read_observations())
        elif self.path == "/api/gcp/report":
            if os.path.isfile(GCP_REPORT_PATH):
                try:
                    with open(GCP_REPORT_PATH, encoding="utf-8") as handle:
                        self.send_json(json.load(handle))
                except (OSError, ValueError) as e:
                    self.send_json({"error": f"Report nicht lesbar: {e}"}, 500)
            else:
                self.send_json({"error": "Noch kein Report vorhanden. Bitte Matrix berechnen."}, 404)
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == "/api/script/run":
            content_len = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(content_len).decode()) if content_len else {}
            script_id = body.get("script_id", "")
            script_info = next((s for s in SCRIPTS_INFO if s["id"] == script_id), None)
            if not script_info:
                self.send_json({"error": "Script not found"}, 404)
                return
            script_path = os.path.join(PROJECT_ROOT, script_info["name"])
            if not os.path.isfile(script_path):
                self.send_json({"error": f"Script file not found: {script_path}"}, 404)
                return
            session_id = str(uuid.uuid4())
            with script_sessions_lock:
                script_sessions[session_id] = {
                    "queue": queue.Queue(),
                    "process": None,
                    "cancel": False,
                    "script_id": script_id,
                    "log": [] # Persistent log of terminal output for page refreshes
                }
            t = threading.Thread(target=run_script_thread, args=(script_path, session_id, script_info.get("args", [])), daemon=True)
            t.start()
            self.send_json({"session_id": session_id, "script_id": script_id})
        elif self.path.startswith("/api/script/input/"):
            session_id = self.path.split("/")[-1]
            content_len = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(content_len).decode()) if content_len else {}
            text = body.get("input", "")
            ok = send_script_input(session_id, text)
            self.send_json({"sent": ok})
        elif self.path == "/api/script/stop":
            content_len = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(content_len).decode()) if content_len else {}
            session_id = body.get("session_id", "")
            with script_sessions_lock:
                if session_id in script_sessions:
                    script_sessions[session_id]["cancel"] = True
                    proc = script_sessions[session_id].get("process")
                    if proc:
                        try:
                            os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
                        except (ProcessLookupError, OSError):
                            try:
                                proc.terminate()
                            except Exception:
                                pass
            self.send_json({"stopped": True})
        elif self.path == "/api/upload":
            self.handle_upload()
        elif self.path == "/api/gcp/observation":
            self._gcp_upsert_observation()
        elif self.path == "/api/gcp/observation/delete":
            self._gcp_delete_observation()
        elif self.path == "/api/gcp/compute":
            self._gcp_compute()
        else:
            self.send_json({"error": "Not found"}, 404)

    # Allowed upload targets (whitelist!) - key is the 'target' form value
    UPLOAD_TARGETS = {
        "matrix_screenshot": {
            "dir": "01_raw",
            "filename": "matrix_screenshot",   # extension appended from upload
            "extensions": [".png", ".jpg", ".jpeg"],
        },
        "raw_video": {
            "dir": "01_raw",
            "filename": None,                    # keep original (sanitized) name
            "extensions": [".mp4", ".mov"],
        },
        "raw_image": {
            "dir": "01_raw",
            "filename": None,
            "extensions": [".png", ".jpg", ".jpeg"],
        },
        "gcp_csv": {
            "dir": "01_raw",
            "filename": None,
            "extensions": [".csv", ".txt"],
        },
        "matrix_txt": {
            "dir": "04_sfm",
            "filename": "matrix",
            "extensions": [".txt"],
        },
    }

    def _stream_multipart(self, boundary, total_len, file_tmp_dir):
        """Stream-parse a multipart/form-data body from self.rfile.

        Writes the ``file`` part to a temp file in ``file_tmp_dir`` and returns
        ``(target_value, file_tmp_path, filename, file_size)``. Only the small
        ``target`` field is held in memory; the (potentially multi-GB) file
        payload is streamed to disk in 64 KiB chunks so the upload never needs
        to fit in RAM as a single blob.
        """
        delim = ("--" + boundary).encode()
        end_marker = b"\r\n" + delim
        crlfcrlf = b"\r\n\r\n"
        remaining = total_len
        buf = b""

        def read_more():
            nonlocal buf, remaining
            if remaining <= 0:
                return False
            chunk = self.rfile.read(min(1 << 16, remaining))
            if not chunk:
                remaining = 0
                return False
            buf += chunk
            remaining -= len(chunk)
            return True

        # Skip the preamble up to the first boundary line.
        while delim not in buf:
            if not read_more():
                break
        idx = buf.find(delim)
        if idx < 0:
            raise ValueError("Keine Multipart-Boundary gefunden")
        buf = buf[idx + len(delim):]
        if buf.startswith(b"\r\n"):
            buf = buf[2:]

        target_value = None
        file_tmp_path = None
        filename = None
        file_size = 0

        while True:
            # Read this part's headers.
            while crlfcrlf not in buf:
                if not read_more():
                    break
            hidx = buf.find(crlfcrlf)
            if hidx < 0:
                break
            raw_headers = buf[:hidx].decode("utf-8", errors="replace")
            buf = buf[hidx + 4:]

            field_name = None
            is_file = False
            part_filename = None
            for line in raw_headers.split("\r\n"):
                if line.lower().startswith("content-disposition:"):
                    for tok in line.split(";"):
                        tok = tok.strip()
                        if tok.startswith("name="):
                            field_name = tok[5:].strip('"')
                        elif tok.startswith("filename="):
                            part_filename = tok[9:].strip('"')
                            is_file = True

            if is_file:
                tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".upload", dir=file_tmp_dir)
                file_tmp_path = tmp.name
                file_size = 0
                filename = part_filename
                while True:
                    eidx = buf.find(end_marker)
                    if eidx >= 0:
                        tmp.write(buf[:eidx])
                        file_size += eidx
                        buf = buf[eidx + len(end_marker):]
                        break
                    # Keep a tail as long as the marker to avoid splitting it
                    # across reads, then flush the safe prefix to the temp file.
                    safe = len(buf) - len(end_marker)
                    if safe > 0:
                        tmp.write(buf[:safe])
                        file_size += safe
                        buf = buf[safe:]
                    if not read_more():
                        # Truncated upload (no closing marker): flush the rest.
                        tmp.write(buf)
                        file_size += len(buf)
                        buf = b""
                        break
                tmp.close()
            else:
                content = b""
                while True:
                    eidx = buf.find(end_marker)
                    if eidx >= 0:
                        content += buf[:eidx]
                        buf = buf[eidx + len(end_marker):]
                        break
                    content += buf
                    buf = b""
                    if not read_more():
                        break
                if field_name == "target":
                    target_value = content.decode("utf-8", errors="replace").strip()

            # After the end marker: either '--' (closing) or '\r\n' (next part).
            if buf.startswith(b"--"):
                break
            if buf.startswith(b"\r\n"):
                buf = buf[2:]

        return target_value, file_tmp_path, filename, file_size

    def handle_upload(self):
        """Receive a multipart/form-data upload (drag & drop) and store it into
        the whitelisted data folder. The file payload is streamed to a temp file
        in 64 KiB chunks so large videos never need to fit in memory."""
        file_tmp_path = None
        try:
            content_type = self.headers.get("Content-Type", "")
            if "multipart/form-data" not in content_type:
                self.send_json({"error": "Erwarte multipart/form-data"}, 400)
                return
            boundary = content_type.split("boundary=")[-1].strip().strip('"')
            if not boundary:
                self.send_json({"error": "Boundary fehlt"}, 400)
                return
            content_len = int(self.headers.get("Content-Length", 0))
            if content_len <= 0:
                self.send_json({"error": "Leerer Upload"}, 400)
                return

            # Temp dir inside the project root -> the final os.replace is a fast
            # same-filesystem rename, not a cross-mount copy.
            upload_tmp_root = os.path.join(PROJECT_ROOT, ".upload_tmp")
            os.makedirs(upload_tmp_root, exist_ok=True)
            target_key, file_tmp_path, orig_filename, file_size = self._stream_multipart(
                boundary, content_len, upload_tmp_root
            )

            if not target_key or target_key not in self.UPLOAD_TARGETS:
                self.send_json({"error": f"Unbekanntes Upload-Ziel: {target_key}"}, 400)
                return
            if not file_tmp_path or not orig_filename:
                self.send_json({"error": "Keine Datei empfangen"}, 400)
                return

            target = self.UPLOAD_TARGETS[target_key]
            ext = os.path.splitext(orig_filename)[1].lower()
            if ext not in target["extensions"]:
                self.send_json({
                    "error": f"Dateityp {ext} nicht erlaubt. Erlaubt: {', '.join(target['extensions'])}"
                }, 400)
                return

            # Sanitize filename: never allow path traversal
            if target["filename"]:
                final_name = target["filename"] + ext
            else:
                final_name = os.path.basename(orig_filename).replace("..", "_")

            dest_dir = os.path.join(DATA_DIR, target["dir"])
            os.makedirs(dest_dir, exist_ok=True)
            dest_path = os.path.join(dest_dir, final_name)
            os.replace(file_tmp_path, dest_path)
            file_tmp_path = None  # consumed by the rename

            rel = os.path.relpath(dest_path, PROJECT_ROOT)
            self.send_json({
                "saved": True,
                "path": rel,
                "size": file_size,
                "target": target_key,
            })
        except Exception as e:
            self.send_json({"error": f"Upload fehlgeschlagen: {e}"}, 500)
        finally:
            if file_tmp_path and os.path.exists(file_tmp_path):
                try:
                    os.unlink(file_tmp_path)
                except OSError:
                    pass

    def send_json(self, data, status=200):
        safe_send_json(self, data, status)

    def _read_json_body(self):
        content_len = int(self.headers.get("Content-Length", 0))
        if content_len <= 0:
            return {}
        try:
            return json.loads(self.rfile.read(content_len).decode())
        except (ValueError, OSError):
            return {}

    def _gcp_frames(self):
        cams_path = os.path.join(SPARSE_TXT_DIR, "cameras.txt")
        imgs_path = os.path.join(SPARSE_TXT_DIR, "images.txt")
        if not (os.path.isfile(cams_path) and os.path.isfile(imgs_path)):
            return {"error": "Kein COLMAP TXT-Export gefunden. Bitte COLMAP-SfM ausfuehren (erzeugt data/04_sfm/sparse_txt/).", "frames": []}
        cams = _parse_cameras_txt_min(cams_path)
        images = _parse_images_txt_min(imgs_path)
        frames = []
        for img in images:
            cam = cams.get(img["camera_id"])
            if cam is None:
                continue
            center = _camera_center(img["qvec"], img["tvec"])
            frames.append({
                "name": img["name"],
                "width": cam["width"],
                "height": cam["height"],
                "center": [round(c, 4) for c in center],
                "thumb": "/api/file/data/02_frames/" + quote(img["name"], safe=""),
            })
        frames.sort(key=lambda f: f["name"])
        return {"frames": frames}

    def _gcp_points(self):
        rel = _parse_gcp_csv(GCP_RELATIVE_CSV)
        utm = _parse_gcp_csv(GCP_COORDINATES_CSV)
        ids = list(dict.fromkeys(list(rel.keys()) + list(utm.keys())))
        points = []
        for gid in ids:
            r = rel.get(gid) or [None, None, None]
            u = utm.get(gid) or [None, None, None]
            points.append({
                "gcp_id": gid,
                "x_rel": r[0], "y_rel": r[1], "z_rel": r[2],
                "x_utm": u[0], "y_utm": u[1], "z_utm": u[2],
            })
        return {"points": points, "has_relative": bool(rel), "has_utm": bool(utm)}

    def _gcp_upsert_observation(self):
        body = self._read_json_body()
        gcp_id = str(body.get("gcp_id", ""))
        image_name = str(body.get("image_name", ""))
        u = body.get("u")
        v = body.get("v")
        if not gcp_id or not image_name or u is None or v is None:
            self.send_json({"error": "gcp_id, image_name, u, v erforderlich"}, 400)
            return
        try:
            u = float(u)
            v = float(v)
        except (TypeError, ValueError):
            self.send_json({"error": "u und v muessen Zahlen sein"}, 400)
            return
        if not math.isfinite(u) or not math.isfinite(v):
            self.send_json({"error": "u und v muessen endliche Zahlen sein"}, 400)
            return

        relative_points = _parse_gcp_csv(GCP_RELATIVE_CSV)
        if gcp_id not in relative_points:
            self.send_json({
                "error": f"Unbekannter GCP '{gcp_id}'. Erst gcp_relative.csv vorbereiten."
            }, 400)
            return

        frame = next((item for item in self._gcp_frames().get("frames", [])
                      if item["name"] == image_name), None)
        if frame is None:
            self.send_json({"error": f"Unbekannter registrierter Frame: {image_name}"}, 400)
            return
        if not (0 <= u < frame["width"] and 0 <= v < frame["height"]):
            self.send_json({
                "error": f"Pixelkoordinate ausserhalb des Frames ({frame['width']}x{frame['height']})"
            }, 400)
            return

        with GCP_OBS_LOCK:
            obs = _read_observations()
            obs = [o for o in obs if not (str(o.get("gcp_id")) == gcp_id and str(o.get("image_name")) == image_name)]
            obs.append({"gcp_id": gcp_id, "image_name": image_name, "u": u, "v": v})
            _write_observations(obs)
            _invalidate_gcp_registration()
        self.send_json({"saved": True, "count": len(obs)})

    def _gcp_delete_observation(self):
        body = self._read_json_body()
        gcp_id = str(body.get("gcp_id", ""))
        image_name = str(body.get("image_name", ""))
        if not gcp_id or not image_name:
            self.send_json({"error": "gcp_id und image_name erforderlich"}, 400)
            return
        with GCP_OBS_LOCK:
            obs = _read_observations()
            before = len(obs)
            obs = [o for o in obs if not (str(o.get("gcp_id")) == gcp_id and str(o.get("image_name")) == image_name)]
            if len(obs) < before:
                _write_observations(obs)
                _invalidate_gcp_registration()
        self.send_json({"deleted": len(obs) < before, "count": len(obs)})

    def _gcp_compute(self):
        if not os.path.isfile(os.path.join(SPARSE_TXT_DIR, "cameras.txt")):
            self.send_json({"error": "Kein COLMAP TXT-Export (data/04_sfm/sparse_txt/). Erst SfM ausfuehren."}, 400)
            return
        if not _read_observations():
            self.send_json({"error": "Keine Beobachtungen. Bitte GCPs in Bildern markieren."}, 400)
            return

        # Common args for both paths.
        common_args = [
            "--sfm-txt", SPARSE_TXT_DIR,
            "--observations", GCP_OBS_PATH,
            "--gcp-relative", GCP_RELATIVE_CSV,
            "--output-matrix", os.path.join(SFM_DIR, "matrix.txt"),
            "--report", GCP_REPORT_PATH,
        ]
        docker_cmd = ["docker", "compose", "run", "--rm", "post-processing",
                      "python3", "/app/src/python/gcp_register.py", *common_args]
        native_cmd = ["python3",
                      os.path.join(PROJECT_ROOT, "src", "python", "gcp_register.py"),
                      *common_args]

        proc, mode = None, None
        try:
            proc = subprocess.run(docker_cmd, cwd=PROJECT_ROOT,
                                  capture_output=True, text=True, timeout=180)
            mode = "docker"
        except FileNotFoundError:
            # docker is not installed / not in PATH; fall back to native python3.
            try:
                proc = subprocess.run(native_cmd, cwd=PROJECT_ROOT,
                                      capture_output=True, text=True, timeout=60)
                mode = "native"
            except FileNotFoundError:
                self.send_json({"error": "Weder 'docker' noch 'python3' sind verfuegbar."}, 500)
                return
        except subprocess.TimeoutExpired:
            self.send_json({"error": "Timeout bei der Berechnung (docker >180s)"}, 504)
            return

        if proc.returncode != 0:
            # docker failed -> try native as a fallback (e.g. WSL without docker integration,
            # missing numpy inside container, etc.). Only fall back once.
            if mode == "docker":
                try:
                    proc2 = subprocess.run(native_cmd, cwd=PROJECT_ROOT,
                                           capture_output=True, text=True, timeout=60)
                    if proc2.returncode == 0:
                        proc, mode = proc2, "native"
                    else:
                        self.send_json({"error": "gcp_register fehlgeschlagen (docker + native)",
                                        "docker_stderr": proc.stderr[-2000:],
                                        "native_stderr": proc2.stderr[-2000:]}, 500)
                        return
                except FileNotFoundError:
                    self.send_json({"error": "gcp_register fehlgeschlagen (docker); python3 fehlt fuer Fallback",
                                    "stderr": proc.stderr[-2000:]}, 500)
                    return
            else:
                self.send_json({"error": "gcp_register fehlgeschlagen",
                                "stderr": proc.stderr[-2000:], "stdout": proc.stdout[-2000:]}, 500)
                return

        if not os.path.isfile(GCP_REPORT_PATH):
            self.send_json({"error": f"Berechnung lief ({mode}), aber kein Report geschrieben",
                            "stdout": proc.stdout[-2000:]}, 500)
            return
        try:
            with open(GCP_REPORT_PATH, encoding="utf-8") as handle:
                report = json.load(handle)
            report["compute_mode"] = mode
            self.send_json(report)
        except (OSError, ValueError) as e:
            self.send_json({"error": f"Report nicht lesbar: {e}"}, 500)

    def do_DELETE(self):
        if self.path == "/api/gcp/observation":
            self._gcp_delete_observation()
        else:
            self.send_json({"error": "Not found"}, 404)

    def log_message(self, format, *args):
        pass


class ThreadingHTTPServerV(ThreadingMixIn, HTTPServer):
    """Threaded server: each request gets its own thread. Essential because
    SSE terminal streams are long-lived connections - without threading a
    single running script would block all other API calls and uploads."""
    daemon_threads = True
    allow_reuse_address = True  # FIX: instantly reuse port 8080 if restarted!


def main():
    host = "0.0.0.0"
    port = 8080
    print(f" Pipeline Dashboard: http://localhost:{port}")
    print(f" Datenverzeichnis: {DATA_DIR}")
    print(" Drück Ctrl+C zum Beenden")
    server = ThreadingHTTPServerV((host, port), DashboardHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()


if __name__ == "__main__":
    main()
