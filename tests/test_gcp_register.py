"""Synthetic unit tests for gcp_register (triangulation + Umeyama + refinement).

Generates known camera poses and GCP 3D points, projects them to pixels (with
optional noise), and checks that triangulation + the Umeyama similarity fit
recover the known transform to a tight tolerance. Requires numpy.
"""

import math
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src", "python"))

try:
    import numpy as np
    from gcp_register import (parse_cameras_txt, parse_images_txt, project_point,
                              quat_to_rotmat, refine_point, triangulate, umeyama, undistort_pixel)
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False


def _rotmat_to_quat(R):
    """Full Shepperd's method (all quadrants) — used only by the tests."""
    tr = R[0, 0] + R[1, 1] + R[2, 2]
    if tr > 0:
        S = math.sqrt(tr + 1.0) * 2
        return [0.25 * S, (R[2, 1] - R[1, 2]) / S, (R[0, 2] - R[2, 0]) / S, (R[1, 0] - R[0, 1]) / S]
    if R[0, 0] > R[1, 1] and R[0, 0] > R[2, 2]:
        S = math.sqrt(1.0 + R[0, 0] - R[1, 1] - R[2, 2]) * 2
        return [(R[2, 1] - R[1, 2]) / S, 0.25 * S, (R[0, 1] + R[1, 0]) / S, (R[0, 2] + R[2, 0]) / S]
    if R[1, 1] > R[2, 2]:
        S = math.sqrt(1.0 + R[1, 1] - R[0, 0] - R[2, 2]) * 2
        return [(R[0, 2] - R[2, 0]) / S, (R[0, 1] + R[1, 0]) / S, 0.25 * S, (R[1, 2] + R[2, 1]) / S]
    S = math.sqrt(1.0 + R[2, 2] - R[0, 0] - R[1, 1]) * 2
    return [(R[1, 0] - R[0, 1]) / S, (R[0, 2] + R[2, 0]) / S, (R[1, 2] + R[2, 1]) / S, 0.25 * S]


@unittest.skipUnless(HAS_NUMPY, "numpy nicht installiert")
class ParseTests(unittest.TestCase):
    def test_parse_images_txt_handles_empty_points_lines(self):
        import tempfile
        fd, path = tempfile.mkstemp(suffix=".txt")
        os.close(fd)
        try:
            with open(path, "w") as fh:
                fh.write("# Image list\n")
                for i in range(6):
                    fh.write(f"{i+1} 1 0 0 0 0 0 0 1 frame_{i:05d}.jpg\n")
                    fh.write("\n")  # empty 2D-points line (common in real COLMAP output)
            images = parse_images_txt(path)
            self.assertEqual(len(images), 6, msg="empty points lines broke the pose/pairing alignment")
            self.assertEqual(images[3]["name"], "frame_00003.jpg")
        finally:
            os.unlink(path)

    def test_parse_cameras_txt_simple_pinhole(self):
        import tempfile
        fd, path = tempfile.mkstemp(suffix=".txt")
        os.close(fd)
        try:
            with open(path, "w") as fh:
                fh.write("# Camera list\n")
                fh.write("1 SIMPLE_PINHOLE 1920 1080 3 800.0 960.0 540.0\n")
            cams = parse_cameras_txt(path)
            self.assertIn(1, cams)
            self.assertEqual(cams[1]["model"], "SIMPLE_PINHOLE")
            self.assertEqual(cams[1]["params"], [800.0, 960.0, 540.0])
        finally:
            os.unlink(path)


@unittest.skipUnless(HAS_NUMPY, "numpy nicht installiert (Test wird in Container E / venv ausgefuehrt)")
class GeometryTests(unittest.TestCase):
    def _make_cameras(self, n=6, radius=8.0, height=4.0):
        """n cameras on a circle looking at the origin (world-to-camera poses)."""
        cams = []
        for i in range(n):
            angle = 2 * math.pi * i / n
            center = np.array([radius * math.cos(angle), radius * math.sin(angle), height])
            # Look at origin: camera z-axis = (origin - center)/||..|| (points into scene).
            forward = -center / np.linalg.norm(center)
            up = np.array([0.0, 0.0, 1.0])
            right = np.cross(forward, up)
            right = right / np.linalg.norm(right)
            true_up = np.cross(right, forward)
            # World-to-camera rotation: rows are (right, -true_up, forward) in COLMAP
            # convention (camera looks along +z in camera space).
            R = np.vstack([right, -true_up, forward])
            t = -R @ center
            cams.append({"R": R, "tvec": t, "center": center,
                         "model": "SIMPLE_PINHOLE", "params": [800.0, 960.0, 540.0],
                         "width": 1920, "height": 1080})
        return cams

    def test_quat_rotmat_roundtrip_is_orthogonal(self):
        R = quat_to_rotmat([1.0, 0.0, 0.0, 0.0])  # identity quaternion
        self.assertTrue(np.allclose(R, np.eye(3)))
        # A random quaternion must produce an orthogonal matrix with det +1.
        q = np.array([0.7, 0.1, -0.3, 0.5])
        q = q / np.linalg.norm(q)
        R = quat_to_rotmat(q.tolist())
        self.assertTrue(np.allclose(R @ R.T, np.eye(3), atol=1e-9))
        self.assertAlmostEqual(np.linalg.det(R), 1.0, places=9)

    def test_rotmat_quat_rotmat_roundtrip(self):
        # rotmat -> quat -> rotmat must recover R exactly for several rotations
        # (covers all trace quadrants, including tr <= 0).
        rng = np.random.default_rng(123)
        for _ in range(20):
            # build a random rotation via two random axis-angle quats
            q = rng.normal(size=4)
            q = q / np.linalg.norm(q)
            R = quat_to_rotmat(q.tolist())
            q2 = _rotmat_to_quat(R)
            R2 = quat_to_rotmat(q2)
            self.assertTrue(np.allclose(R, R2, atol=1e-9),
                            msg=f"roundtrip failed, max diff {np.abs(R - R2).max()}")

    def test_undistort_pinhole_is_identity(self):
        # SIMPLE_PINHOLE with the principal point at the marked pixel -> (0,0).
        x, y = undistort_pixel("SIMPLE_PINHOLE", [800.0, 960.0, 540.0], 960.0, 540.0)
        self.assertAlmostEqual(x, 0.0)
        self.assertAlmostEqual(y, 0.0)

    def test_triangulation_recovers_known_point(self):
        cams = self._make_cameras(n=6)
        X_true = np.array([1.0, -0.5, 0.3])
        rays = []
        for cam in cams:
            uv = project_point(X_true, cam["R"], cam["tvec"], cam["model"], cam["params"])
            x, y = undistort_pixel(cam["model"], cam["params"], uv[0], uv[1])
            d = cam["R"].T @ np.array([x, y, 1.0])
            d = d / np.linalg.norm(d)
            rays.append((cam["center"], d))
        X = triangulate(rays)
        self.assertTrue(np.allclose(X, X_true, atol=1e-6),
                        msg=f"triangulation off by {np.linalg.norm(X - X_true)}")

    def test_refinement_improves_noisy_pixels(self):
        cams = self._make_cameras(n=6)
        X_true = np.array([0.7, 0.2, -0.1])
        pixels = [project_point(X_true, cam["R"], cam["tvec"], cam["model"], cam["params"])
                  for cam in cams]
        # Add 1 px gaussian noise to the marks.
        rng = np.random.default_rng(42)
        noisy = [uv + rng.normal(0.0, 1.0, 2) for uv in pixels]
        cam_meta = [(cam["R"], cam["tvec"], cam["model"], cam["params"]) for cam in cams]
        # Initial triangulation from the noisy rays.
        rays = []
        for cam, uv in zip(cams, noisy):
            x, y = undistort_pixel(cam["model"], cam["params"], uv[0], uv[1])
            d = cam["R"].T @ np.array([x, y, 1.0])
            rays.append((cam["center"], d / np.linalg.norm(d)))
        X0 = triangulate(rays)
        X_refined = refine_point(X0, cam_meta, noisy)
        err0 = np.linalg.norm(X0 - X_true)
        err1 = np.linalg.norm(X_refined - X_true)
        self.assertLess(err1, err0,
                        msg=f"refinement did not improve: {err0} -> {err1}")
        self.assertLess(err1, 0.02, msg=f"refined point too far from truth: {err1}")

    def test_umeyama_recovers_known_similarity(self):
        rng = np.random.default_rng(7)
        X_src = rng.uniform(-5, 5, (5, 3))
        # Known rotation (30 deg about z) + scale 2.5 + translation.
        theta = math.radians(30.0)
        R_true = np.array([[math.cos(theta), -math.sin(theta), 0.0],
                           [math.sin(theta), math.cos(theta), 0.0],
                           [0.0, 0.0, 1.0]])
        s_true, t_true = 2.5, np.array([100.0, 200.0, 5.0])
        X_dst = (s_true * (R_true @ X_src.T)).T + t_true
        s, R, t = umeyama(X_src, X_dst)
        self.assertAlmostEqual(s, s_true, places=9)
        self.assertTrue(np.allclose(R, R_true, atol=1e-9))
        self.assertTrue(np.allclose(t, t_true, atol=1e-9))

    def test_end_to_end_pipeline_recovers_transform(self):
        """Full chain: project GCPs -> mark -> triangulate -> Umeyama -> compare."""
        cams = self._make_cameras(n=6)
        # GCPs in the SfM frame and a known similarity to relative UTM.
        gcp_sfm = np.array([[1.0, 0.0, 0.2], [0.0, 1.0, -0.1], [-1.0, 0.3, 0.0],
                            [0.5, -1.2, 0.4], [2.0, 1.5, -0.3]])
        theta = math.radians(25.0)
        R_true = np.array([[math.cos(theta), 0.0, math.sin(theta)],
                           [0.0, 1.0, 0.0],
                           [-math.sin(theta), 0.0, math.cos(theta)]])
        s_true, t_true = 3.1, np.array([50.0, -30.0, 12.0])
        gcp_rel = (s_true * (R_true @ gcp_sfm.T)).T + t_true

        # Mark each GCP in all 6 cameras (noise-free).
        sfm_points = []
        for X_true in gcp_sfm:
            rays = []
            for cam in cams:
                uv = project_point(X_true, cam["R"], cam["tvec"], cam["model"], cam["params"])
                x, y = undistort_pixel(cam["model"], cam["params"], uv[0], uv[1])
                d = cam["R"].T @ np.array([x, y, 1.0])
                rays.append((cam["center"], d / np.linalg.norm(d)))
            sfm_points.append(triangulate(rays))
        sfm_points = np.array(sfm_points)

        s, R, t = umeyama(sfm_points, gcp_rel)
        self.assertAlmostEqual(s, s_true, places=6)
        self.assertTrue(np.allclose(R, R_true, atol=1e-7))
        self.assertTrue(np.allclose(t, t_true, atol=1e-6))
        # Residuals must be ~0 (noise-free).
        fitted = (s * (R @ sfm_points.T)).T + t
        self.assertLess(np.linalg.norm(fitted - gcp_rel), 1e-6)


if __name__ == "__main__":
    unittest.main()
