"""Unit tests for the B-spline fitting in centerline_bspline."""

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src", "python"))

from centerline_bspline import bspline, remove_consecutive_duplicates


class BsplineTests(unittest.TestCase):
    def test_endpoints_are_preserved(self):
        points = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [2.0, 0.0, 0.0]]
        smoothed = bspline(points, samples_per_segment=4, degree=3)
        self.assertEqual(smoothed[0], [0.0, 0.0, 0.0])
        self.assertEqual(smoothed[-1], [2.0, 0.0, 0.0])

    def test_linear_input_stays_on_line(self):
        points = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [2.0, 0.0, 0.0]]
        smoothed = bspline(points, samples_per_segment=4, degree=3)
        for point in smoothed:
            self.assertAlmostEqual(point[1], 0.0)
            self.assertAlmostEqual(point[2], 0.0)

    def test_too_few_points_falls_back_to_linear(self):
        points = [[0.0, 0.0, 0.0], [2.0, 0.0, 0.0]]
        smoothed = bspline(points, samples_per_segment=3, degree=3)
        self.assertEqual(smoothed[0], [0.0, 0.0, 0.0])
        self.assertEqual(smoothed[-1], [2.0, 0.0, 0.0])
        self.assertGreaterEqual(len(smoothed), 2)

    def test_remove_consecutive_duplicates(self):
        points = [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [1.0, 0.0, 0.0]]
        self.assertEqual(remove_consecutive_duplicates(points), [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0]])


if __name__ == "__main__":
    unittest.main()
