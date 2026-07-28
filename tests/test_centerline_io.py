"""Unit tests for centerline_io (shared CSV reader/writer)."""

import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src", "python"))

from centerline_io import iter_points, read_centerline, write_centerline


class ReadCenterlineTests(unittest.TestCase):
    def test_read_headered_groups_by_branch(self):
        with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, newline="") as handle:
            handle.write("branch_id,component_id,x,y,z\n")
            handle.write("0,0,0,0,0\n0,0,1,0,0\n1,0,5,5,5\n1,0,6,5,5\n")
            path = handle.name
        try:
            paths = read_centerline(path)
            self.assertEqual(list(paths.keys()), [("0", "0"), ("1", "0")])
            self.assertEqual(paths[("0", "0")], [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0]])
            self.assertEqual(paths[("1", "0")], [[5.0, 5.0, 5.0], [6.0, 5.0, 5.0]])
        finally:
            os.unlink(path)

    def test_read_headerless_defaults_branch_component(self):
        with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, newline="") as handle:
            handle.write("0,0,0\n1,0,0\n2,0,0\n")
            path = handle.name
        try:
            paths = read_centerline(path)
            self.assertEqual(list(paths.keys()), [("0", "0")])
            self.assertEqual(paths[("0", "0")], [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [2.0, 0.0, 0.0]])
        finally:
            os.unlink(path)

    def test_read_empty_raises(self):
        with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, newline="") as handle:
            handle.write("")
            path = handle.name
        try:
            with self.assertRaises(ValueError):
                read_centerline(path)
        finally:
            os.unlink(path)

    def test_iter_points_yields_grouped_points(self):
        with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, newline="") as handle:
            handle.write("branch_id,component_id,x,y,z\n")
            handle.write("0,0,0,0,0\n0,0,1,0,0\n1,0,5,5,5\n")
            path = handle.name
        try:
            rows = list(iter_points(path))
            # iter_points groups by (branch_id, component_id) and preserves order within each branch.
            self.assertEqual(rows[0], ("0", "0", [0.0, 0.0, 0.0]))
            self.assertEqual(rows[1], ("0", "0", [1.0, 0.0, 0.0]))
            self.assertEqual(rows[2], ("1", "0", [5.0, 5.0, 5.0]))
        finally:
            os.unlink(path)


class WriteCenterlineTests(unittest.TestCase):
    def test_write_then_read_roundtrip(self):
        from collections import OrderedDict
        ordered = OrderedDict()
        ordered[("0", "0")] = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0]]
        ordered[("1", "0")] = [[5.0, 5.0, 5.0], [6.0, 5.0, 5.0]]
        with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, newline="") as handle:
            path = handle.name
        try:
            total = write_centerline(path, ordered)
            self.assertEqual(total, 4)
            reread = read_centerline(path)
            self.assertEqual(reread, ordered)
        finally:
            os.unlink(path)

    def test_write_has_canonical_header(self):
        from collections import OrderedDict
        ordered = OrderedDict()
        ordered[("0", "0")] = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0]]
        with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, newline="") as handle:
            path = handle.name
        try:
            write_centerline(path, ordered)
            with open(path, encoding="utf-8") as handle:
                self.assertEqual(handle.readline().strip(), "branch_id,component_id,x,y,z")
        finally:
            os.unlink(path)


if __name__ == "__main__":
    unittest.main()
