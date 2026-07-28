"""GCP registration from image markings + COLMAP poses.

Replaces the manual CloudCompare point-picking step with a multi-view image
marking workflow: the user marks each GCP in several registered frames (stored
in ``gcp_observations.json`` by the web UI); this script

  1. undistorts the marked pixels with the COLMAP camera model,
  2. triangulates each GCP's 3D position in the SfM frame (least-squares over
     all viewing rays), with optional per-GCP reprojection refinement
     (Gauss-Newton, camera poses fixed),
  3. estimates the 7-parameter similarity transform (s, R, t) mapping SfM
     coordinates to the relative UTM frame (anchor-centered) via the Umeyama
     closed-form solution,
  4. writes ``matrix.txt`` in the existing 4x4 format consumed by
     ``transform_centerline.py`` (downstream unchanged) and a ``gcp_report.json``
     with per-observation reprojection errors (px) and per-GCP residuals (m).

The relative GCP coordinates and the anchor are produced by ``prepare_gcp.py``
from ``gcp_coordinates.csv``.
"""

import argparse
import csv
import json
import math
import os
from typing import Dict, List, Tuple

import numpy as np

Point = np.ndarray  # shape (3,)


# --- COLMAP TXT parsing -------------------------------------------------------

def parse_cameras_txt(path: str) -> Dict[int, dict]:
    cameras = {}
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split()
            cam_id = int(parts[0])
            model = parts[1]
            width = int(parts[2])
            height = int(parts[3])
            num_params = int(parts[4])
            params = [float(x) for x in parts[5:5 + num_params]]
            cameras[cam_id] = {"model": model, "width": width, "height": height, "params": params}
    return cameras


def parse_images_txt(path: str) -> List[dict]:
    # Each image occupies two consecutive lines: the pose line and the
    # 2D-points line (which may be empty). We keep empty points lines so the
    # pairing stays aligned and only drop comment lines; a blank "pose" slot
    # (stray points line / trailing blank) is skipped.
    with open(path, encoding="utf-8") as handle:
        lines = [line.rstrip("\n") for line in handle if not line.lstrip().startswith("#")]
    images = []
    for i in range(0, len(lines), 2):
        parts = lines[i].split()
        if not parts:
            continue
        images.append({
            "image_id": int(parts[0]),
            "qvec": [float(x) for x in parts[1:5]],
            "tvec": [float(x) for x in parts[5:8]],
            "camera_id": int(parts[8]),
            "name": parts[9],
        })
    return images


def parse_gcp_relative(path: str) -> Dict[str, np.ndarray]:
    """Read the relative-GCP CSV (produced by prepare_gcp.py) -> {gcp_id: [x, y, z]}."""
    with open(path, encoding="utf-8") as handle:
        reader = csv.reader(handle)
        header = [h.strip() for h in next(reader)]
        lower = [h.lower() for h in header]
        id_idx = next((i for i, c in enumerate(lower) if c in ("id", "name", "gcp", "passpunkt")), None)
        x_idx = next((i for i, c in enumerate(lower) if c in ("x", "east", "ost", "easting")), None)
        y_idx = next((i for i, c in enumerate(lower) if c in ("y", "north", "nord", "northing")), None)
        z_idx = next((i for i, c in enumerate(lower) if c in ("z", "height", "hoehe", "elevation")), None)
        if None in (id_idx, x_idx, y_idx, z_idx):
            raise ValueError(f"{path}: konnte id/x/y/z-Spalten nicht erkennen (Header: {header})")
        points = {}
        for row in reader:
            if not row:
                continue
            gcp_id = row[id_idx].strip()
            points[gcp_id] = np.array([float(row[x_idx]), float(row[y_idx]), float(row[z_idx])])
    return points


# --- Geometry helpers ---------------------------------------------------------

def quat_to_rotmat(q: List[float]) -> np.ndarray:
    qw, qx, qy, qz = q
    return np.array([
        [1 - 2 * (qy * qy + qz * qz), 2 * (qx * qy - qz * qw), 2 * (qx * qz + qy * qw)],
        [2 * (qx * qy + qz * qw), 1 - 2 * (qx * qx + qz * qz), 2 * (qy * qz - qx * qw)],
        [2 * (qx * qz - qy * qw), 2 * (qy * qz + qx * qw), 1 - 2 * (qx * qx + qy * qy)],
    ])


def undistort_pixel(model: str, params: List[float], u: float, v: float) -> Tuple[float, float]:
    """Map a distorted pixel to normalized, undistorted camera coordinates (x, y, 1)."""
    if model == "SIMPLE_PINHOLE":
        f, cx, cy = params
        return (u - cx) / f, (v - cy) / f
    if model == "PINHOLE":
        fx, fy, cx, cy = params
        return (u - cx) / fx, (v - cy) / fy
    if model == "SIMPLE_RADIAL":
        f, cx, cy, k1 = params
        xd, yd = (u - cx) / f, (v - cy) / f
        x, y = xd, yd
        for _ in range(15):
            r2 = x * x + y * y
            x = xd / (1 + k1 * r2)
            y = yd / (1 + k1 * r2)
        return x, y
    if model == "RADIAL":
        f, cx, cy, k1, k2 = params
        xd, yd = (u - cx) / f, (v - cy) / f
        x, y = xd, yd
        for _ in range(20):
            r2 = x * x + y * y
            inv = 1 + k1 * r2 + k2 * r2 * r2
            x = xd / inv
            y = yd / inv
        return x, y
    if model == "OPENCV":
        fx, fy, cx, cy, k1, k2, p1, p2 = params
        xd, yd = (u - cx) / fx, (v - cy) / fy
        x, y = xd, yd
        for _ in range(20):
            r2 = x * x + y * y
            radial = 1 + k1 * r2 + k2 * r2 * r2
            tx = 2 * p1 * x * y + p2 * (r2 + 2 * x * x)
            ty = p1 * (r2 + 2 * y * y) - 2 * p2 * x * y
            x = (xd - tx) / radial
            y = (yd - ty) / radial
        return x, y
    raise ValueError(
        f"Kameramodell '{model}' wird von gcp_register nicht unterstuetzt "
        "(nur SIMPLE_PINHOLE, PINHOLE, SIMPLE_RADIAL, RADIAL, OPENCV)."
    )


def project_point(X_world: np.ndarray, R: np.ndarray, tvec: np.ndarray,
                  model: str, params: List[float]) -> np.ndarray:
    """Project a world point to a distorted pixel (forward model)."""
    Xc = R @ X_world + tvec
    if abs(Xc[2]) < 1e-12:
        return np.array([float("nan"), float("nan")])
    x, y = Xc[0] / Xc[2], Xc[1] / Xc[2]
    if model == "SIMPLE_PINHOLE":
        f, cx, cy = params
        return np.array([f * x + cx, f * y + cy])
    if model == "PINHOLE":
        fx, fy, cx, cy = params
        return np.array([fx * x + cx, fy * y + cy])
    if model == "SIMPLE_RADIAL":
        f, cx, cy, k1 = params
        r2 = x * x + y * y
        return np.array([f * x * (1 + k1 * r2) + cx, f * y * (1 + k1 * r2) + cy])
    if model == "RADIAL":
        f, cx, cy, k1, k2 = params
        r2 = x * x + y * y
        d = 1 + k1 * r2 + k2 * r2 * r2
        return np.array([f * x * d + cx, f * y * d + cy])
    if model == "OPENCV":
        fx, fy, cx, cy, k1, k2, p1, p2 = params
        r2 = x * x + y * y
        d = 1 + k1 * r2 + k2 * r2 * r2
        u = fx * (x * d + 2 * p1 * x * y + p2 * (r2 + 2 * x * x)) + cx
        v = fy * (y * d + p1 * (r2 + 2 * y * y) - 2 * p2 * x * y) + cy
        return np.array([u, v])
    raise ValueError(f"Kameramodell '{model}' wird nicht unterstuetzt.")


def triangulate(rays: List[Tuple[np.ndarray, np.ndarray]]) -> np.ndarray:
    """Least-squares triangulation over viewing rays (camera center C, unit direction d).

    Minimizes the sum of squared perpendicular distances to all rays
    (equivalent to the generalized midpoint method).
    """
    A, b = [], []
    for C, d in rays:
        M = np.eye(3) - np.outer(d, d)
        A.append(M)
        b.append(M @ C)
    A = np.vstack(A)
    b = np.concatenate(b)
    X, *_ = np.linalg.lstsq(A, b, rcond=None)
    return X


def refine_point(X0: np.ndarray, cams: List[Tuple[np.ndarray, np.ndarray, str, List[float]]],
                 pixels: List[np.ndarray], iters: int = 20) -> np.ndarray:
    """Gauss-Newton refinement of a single GCP's 3D position, minimizing the
    reprojection error against the marked pixels (camera poses fixed).
    Finite-difference Jacobian; falls back gracefully if degenerate.
    """
    X = X0.copy().astype(float)
    for _ in range(iters):
        r = np.concatenate([project_point(X, R, t, m, p) - uv
                            for (R, t, m, p), uv in zip(cams, pixels)])
        if not np.all(np.isfinite(r)):
            break
        J = np.zeros((len(r), 3))
        for k in range(3):
            step = 1e-6 * max(1.0, abs(X[k]))
            dX = np.zeros(3)
            dX[k] = step
            rp = np.concatenate([project_point(X + dX, R, t, m, p) - uv
                                 for (R, t, m, p), uv in zip(cams, pixels)])
            J[:, k] = (rp - r) / step
        try:
            dX, *_ = np.linalg.lstsq(J, -r, rcond=None)
        except np.linalg.LinAlgError:
            break
        X = X + dX
        if np.linalg.norm(dX) < 1e-9:
            break
    return X


def umeyama(X_src: np.ndarray, X_dst: np.ndarray) -> Tuple[float, np.ndarray, np.ndarray]:
    """Closed-form 7-parameter similarity (s, R, t) with s*R @ X_src + t ~= X_dst."""
    mu_s = X_src.mean(0)
    mu_d = X_dst.mean(0)
    Xs = X_src - mu_s
    Xd = X_dst - mu_d
    n = X_src.shape[0]
    H = Xs.T @ Xd / n
    U, S, Vt = np.linalg.svd(H)
    d = np.sign(np.linalg.det(Vt.T @ U.T))
    D = np.diag([1.0, 1.0, d])
    R = Vt.T @ D @ U.T
    var_s = np.sum(Xs ** 2) / n
    s = float((S * np.diag(D)).sum() / var_s) if var_s > 1e-12 else 1.0
    t = mu_d - s * R @ mu_s
    return s, R, t


# --- Main pipeline ------------------------------------------------------------

def build_camera_index(images: List[dict], cameras: Dict[int, dict]) -> Dict[str, dict]:
    """Index by image name -> {R, tvec, center, model, params, width, height}."""
    index = {}
    for img in images:
        cam = cameras.get(img["camera_id"])
        if cam is None:
            continue
        R = quat_to_rotmat(img["qvec"])
        t = np.array(img["tvec"])
        center = -R.T @ t
        index[img["name"]] = {
            "R": R, "tvec": t, "center": center,
            "model": cam["model"], "params": cam["params"],
            "width": cam["width"], "height": cam["height"],
        }
    return index


def register_gcps(observations: List[dict], camera_index: Dict[str, dict],
                  gcp_relative: Dict[str, np.ndarray], refine: bool) -> dict:
    """Triangulate GCPs, fit similarity, build report."""
    # Group observations by gcp_id.
    by_gcp: Dict[str, List[dict]] = {}
    for obs in observations:
        by_gcp.setdefault(str(obs["gcp_id"]), []).append(obs)

    sfm_points: Dict[str, np.ndarray] = {}
    per_gcp_report = []
    outliers_dropped = []

    for gcp_id, obs_list in by_gcp.items():
        if gcp_id not in gcp_relative:
            per_gcp_report.append({
                "gcp_id": gcp_id, "num_observations": len(obs_list),
                "status": "skipped", "reason": "keine relativen UTM-Koordinaten gefunden",
            })
            continue

        def build_rays(used_obs):
            rays, cams_meta, pixels = [], [], []
            for obs in used_obs:
                cam = camera_index.get(obs["image_name"])
                if cam is None:
                    continue
                x, y = undistort_pixel(cam["model"], cam["params"], float(obs["u"]), float(obs["v"]))
                direction = cam["R"].T @ np.array([x, y, 1.0])
                direction = direction / np.linalg.norm(direction)
                rays.append((cam["center"], direction))
                cams_meta.append((cam["R"], cam["tvec"], cam["model"], cam["params"]))
                pixels.append(np.array([float(obs["u"]), float(obs["v"])]))
            return rays, cams_meta, pixels

        # Outlier rejection: if we have > 3 usable observations, drop the worst
        # reprojection outlier once (only if it clearly exceeds the median).
        used = obs_list
        if len(used) > 3:
            rays, cams_meta, pixels = build_rays(used)
            if len(rays) >= 2:
                X = triangulate(rays)
                reproj = [np.linalg.norm(project_point(X, R, t, m, p) - uv)
                          for (R, t, m, p), uv in zip(cams_meta, pixels)]
                med = float(np.median(reproj))
                worst_idx = int(np.argmax(reproj))
                if reproj[worst_idx] > max(2.0, 5.0 * med):
                    outliers_dropped.append({
                        "gcp_id": gcp_id, "image_name": used[worst_idx]["image_name"],
                        "reprojection_px": round(reproj[worst_idx], 3),
                    })
                    used = [o for i, o in enumerate(used) if i != worst_idx]

        rays, cams_meta, pixels = build_rays(used)
        if len(rays) < 2:
            per_gcp_report.append({
                "gcp_id": gcp_id, "num_observations": len(rays),
                "status": "skipped", "reason": "weniger als 2 nutzbare Beobachtungen",
            })
            continue

        X = triangulate(rays)
        if refine and len(rays) >= 2:
            X = refine_point(X, cams_meta, pixels)

        reproj_errors = [float(np.linalg.norm(project_point(X, R, t, m, p) - uv))
                         for (R, t, m, p), uv in zip(cams_meta, pixels)]
        reproj_uv = [project_point(X, R, t, m, p).tolist()
                     for (R, t, m, p), uv in zip(cams_meta, pixels)]
        sfm_points[gcp_id] = X
        per_gcp_report.append({
            "gcp_id": gcp_id,
            "num_observations": len(rays),
            "status": "ok",
            "triangulated_sfm": X.tolist(),
            "reprojection_rmse_px": round(float(math.sqrt(sum(e * e for e in reproj_errors) / len(reproj_errors))), 4),
            "max_reprojection_px": round(float(max(reproj_errors)), 4),
            "observations": [
                {"image_name": o["image_name"], "u": float(o["u"]), "v": float(o["v"]),
                 "reprojected_uv": reproj_uv[i], "reprojection_px": round(reproj_errors[i], 4)}
                for i, o in enumerate(used) if i < len(reproj_uv)
            ],
        })

    # Similarity fit on GCPs that have both an SfM point and relative UTM.
    pairs = [(gcp_id, sfm_points[gcp_id], gcp_relative[gcp_id])
             for gcp_id in sfm_points if gcp_id in gcp_relative]
    if len(pairs) < 3:
        raise ValueError(
            f"Zuwenig GCPs mit beiden Koordinaten ({len(pairs)}); mindestens 3 noetig."
        )

    X_sfm = np.array([p[1] for p in pairs])
    X_rel = np.array([p[2] for p in pairs])
    s, R, t = umeyama(X_sfm, X_rel)

    # Per-GCP fit residual in meters.
    fitted = (s * (R @ X_sfm.T)).T + t
    residuals = np.linalg.norm(fitted - X_rel, axis=1)
    total_rmse = float(math.sqrt((residuals ** 2).mean()))
    for (gcp_id, _, _), res in zip(pairs, residuals):
        for entry in per_gcp_report:
            if entry["gcp_id"] == gcp_id:
                entry["fit_residual_m"] = round(float(res), 5)
                break

    matrix_4x4 = np.eye(4)
    matrix_4x4[:3, :3] = s * R
    matrix_4x4[:3, 3] = t

    return {
        "num_gcps_used": len(pairs),
        "num_observations": int(sum(o["num_observations"] for o in per_gcp_report if o.get("status") == "ok")),
        "scale": round(float(s), 8),
        "rotation": R.tolist(),
        "translation": t.tolist(),
        "total_rmse_m": round(total_rmse, 5),
        "max_residual_m": round(float(residuals.max()), 5),
        "per_gcp": per_gcp_report,
        "outliers_dropped": outliers_dropped,
        "matrix_4x4": matrix_4x4.tolist(),
    }


def write_matrix(path: str, matrix: np.ndarray) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        for row in matrix:
            handle.write(", ".join(f"{v:.12g}" for v in row) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Triangulate GCPs from image markings + COLMAP poses and "
                    "estimate the SfM->relative-UTM similarity transform (matrix.txt)."
    )
    parser.add_argument("--sfm-txt", default="/data/04_sfm/sparse_txt",
                        help="Verzeichnis mit cameras.txt und images.txt (COLMAP TXT-Export)")
    parser.add_argument("--observations", default="/data/04_sfm/gcp_observations.json",
                        help="Beobachtungs-JSON der UI [{gcp_id, image_name, u, v}]")
    parser.add_argument("--gcp-relative", default="/data/01_raw/gcp_relative.csv",
                        help="Relative GCP-Koordinaten (von prepare_gcp.py)")
    parser.add_argument("--output-matrix", default="/data/04_sfm/matrix.txt",
                        help="Ausgabe: 4x4 Transformationsmatrix")
    parser.add_argument("--report", default="/data/04_sfm/gcp_report.json",
                        help="Ausgabe: Qualitätsreport JSON")
    parser.add_argument("--refine", dest="refine", action="store_true", default=True,
                        help="Reprojektions-Refinement (Gauss-Newton) pro GCP (Default an)")
    parser.add_argument("--no-refine", dest="refine", action="store_false",
                        help="Reprojektions-Refinement deaktivieren (nur geschlossene Form)")
    args = parser.parse_args()

    cameras_path = os.path.join(args.sfm_txt, "cameras.txt")
    images_path = os.path.join(args.sfm_txt, "images.txt")
    for p in (cameras_path, images_path, args.observations, args.gcp_relative):
        if not os.path.isfile(p):
            raise FileNotFoundError(f"Datei nicht gefunden: {p}")

    cameras = parse_cameras_txt(cameras_path)
    images = parse_images_txt(images_path)
    camera_index = build_camera_index(images, cameras)
    with open(args.observations, encoding="utf-8") as handle:
        observations = json.load(handle)
    gcp_relative = parse_gcp_relative(args.gcp_relative)

    if not observations:
        raise ValueError("Keine GCP-Beobachtungen vorhanden. Bitte in der UI markieren.")

    report = register_gcps(observations, camera_index, gcp_relative, args.refine)

    write_matrix(args.output_matrix, np.array(report["matrix_4x4"]))
    os.makedirs(os.path.dirname(args.report), exist_ok=True)
    report["matrix_path"] = args.output_matrix
    with open(args.report, "w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2, ensure_ascii=False)
        handle.write("\n")

    print(f"matrix.txt geschrieben: {args.output_matrix}")
    print(f"GCPs verwendet: {report['num_gcps_used']}, Beobachtungen: {report['num_observations']}")
    print(f"Total RMSE: {report['total_rmse_m']} m, Max Residuum: {report['max_residual_m']} m, Skalierung: {report['scale']:.6f}")
    if report["outliers_dropped"]:
        print(f"Ausreißer verworfen: {len(report['outliers_dropped'])}")
    print(f"Report: {args.report}")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, FileNotFoundError) as error:
        raise SystemExit(f"Error: {error}")
