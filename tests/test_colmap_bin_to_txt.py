"""Unit tests for colmap_bin_to_txt (bin -> txt converter)."""

import math
import os
import struct
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src", "python"))

from colmap_bin_to_txt import (read_cameras_bin, read_images_bin, pick_largest_model,
                                write_cameras_txt, write_images_txt)


def _write_cameras_bin(path, cameras):
    """cameras: list of (cam_id, model_id, width, height, params)."""
    with open(path, "wb") as fh:
        fh.write(struct.pack("<Q", len(cameras)))
        for cam_id, model_id, width, height, params in cameras:
            fh.write(struct.pack("<iiQQQ", cam_id, model_id, width, height, len(params)))
            fh.write(struct.pack(f"<{len(params)}d", *params))


def _write_images_bin(path, images):
    """images: list of (image_id, qvec[4], tvec[3], camera_id, name, points2d[]).
    points2d: list of (x, y, point3D_id)."""
    with open(path, "wb") as fh:
        fh.write(struct.pack("<Q", len(images)))
        for image_id, qvec, tvec, camera_id, name, points2d in images:
            fh.write(struct.pack("<i", image_id))
            fh.write(struct.pack("<dddd", *qvec))
            fh.write(struct.pack("<ddd", *tvec))
            fh.write(struct.pack("<i", camera_id))
            fh.write(name.encode("utf-8") + b"\x00")
            fh.write(struct.pack("<Q", len(points2d)))
            for x, y, pid in points2d:
                fh.write(struct.pack("<ddq", x, y, pid))


class ColmapBinToTxtTests(unittest.TestCase):
    def test_roundtrip_cameras(self):
        with tempfile.TemporaryDirectory() as tmp:
            cameras_bin = os.path.join(tmp, "cameras.bin")
            _write_cameras_bin(cameras_bin, [
                (1, 0, 1920, 1080, [800.0, 960.0, 540.0]),  # SIMPLE_PINHOLE
                (2, 2, 1920, 1080, [800.0, 960.0, 540.0, 0.0123]),  # SIMPLE_RADIAL
                (3, 4, 1920, 1080, [800.0, 800.0, 960.0, 540.0, 0.01, 0.02, 0.001, 0.002]),  # OPENCV
            ])
            cameras = read_cameras_bin(cameras_bin)
            self.assertEqual(len(cameras), 3)
            self.assertEqual(cameras[1]["model"], "SIMPLE_PINHOLE")
            self.assertEqual(cameras[2]["model"], "SIMPLE_RADIAL")
            self.assertEqual(cameras[2]["params"][3], 0.0123)
            self.assertEqual(cameras[3]["model"], "OPENCV")
            self.assertEqual(cameras[3]["params"], [800.0, 800.0, 960.0, 540.0, 0.01, 0.02, 0.001, 0.002])

    def test_roundtrip_images_with_points2d(self):
        with tempfile.TemporaryDirectory() as tmp:
            images_bin = os.path.join(tmp, "images.bin")
            # identity quaternion (qw=1, rest 0)
            _write_images_bin(images_bin, [
                (1, [1.0, 0.0, 0.0, 0.0], [0.1, 0.2, 0.3], 1, "frame_00000.jpg",
                 [(100.5, 200.25, 42), (300.0, 400.0, -1)]),
                (2, [0.7071, 0.7071, 0.0, 0.0], [-0.5, 0.0, 0.5], 1, "frame_00001.jpg", []),
            ])
            images = list(read_images_bin(images_bin))
            self.assertEqual(len(images), 2)
            img_id, qvec, tvec, cam_id, name = images[0]
            self.assertEqual(img_id, 1)
            self.assertEqual(name, "frame_00000.jpg")
            self.assertEqual(cam_id, 1)
            self.assertEqual(qvec, [1.0, 0.0, 0.0, 0.0])
            self.assertEqual(tvec, [0.1, 0.2, 0.3])

    def test_pick_largest_model_uses_points3D_bin_size(self):
        with tempfile.TemporaryDirectory() as tmp:
            # Two numeric subdirs, points3D.bin sizes: small=100, large=5000
            for name, size in [("0", 100), ("1", 5000)]:
                d = os.path.join(tmp, name)
                os.makedirs(d, exist_ok=True)
                with open(os.path.join(d, "points3D.bin"), "wb") as fh:
                    fh.write(b"\x00" * size)
            # Also create a non-numeric dir that should be ignored.
            os.makedirs(os.path.join(tmp, "manual"))
            chosen = pick_largest_model(tmp)
            self.assertEqual(os.path.basename(chosen), "1")

    def test_pick_largest_model_falls_back_to_root(self):
        with tempfile.TemporaryDirectory() as tmp:
            # cameras.bin directly in root -> that is the model.
            with open(os.path.join(tmp, "cameras.bin"), "wb") as fh:
                fh.write(b"\x00")
            chosen = pick_largest_model(tmp)
            self.assertEqual(chosen, tmp)

    def test_write_cameras_txt_format(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "cameras.txt")
            from colmap_bin_to_txt import COLMAP_MODEL_NAMES
            cameras = {1: {"model": "SIMPLE_PINHOLE", "width": 1920, "height": 1080,
                            "params": [800.0, 960.0, 540.0]}}
            write_cameras_txt(out, cameras)
            text = open(out).read()
            self.assertIn("# Camera list", text)
            self.assertIn("1 SIMPLE_PINHOLE 1920 1080 3 800.0 960.0 540.0", text)

    def test_write_images_txt_format_with_empty_points(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "images.txt")
            images = [(1, [1.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0], 1, "frame_0.jpg")]
            write_images_txt(out, images)
            text = open(out).read()
            lines = text.splitlines()
            # 2 comment lines + 1 pose line + 1 empty 2D-points line = 4; plus a trailing
            # newline yields an empty 5th entry from splitlines() that doesn't exist as
            # a real line, so expect 4 logical lines or 5 split chunks.
            self.assertGreaterEqual(len(lines), 4)
            self.assertIn("1 1.0 0.0 0.0 0.0 0.0 0.0 0.0 1 frame_0.jpg", lines)
            # The empty 2D-points line must be present (gcp_register relies on it).
            self.assertIn("", lines)


if __name__ == "__main__":
    unittest.main()
