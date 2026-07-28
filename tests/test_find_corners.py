"""Unit tests for corner detection and path segmentation in centerline_bspline."""

import math
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src", "python"))

from centerline_bspline import find_corners, segment_path


class FindCornersTests(unittest.TestCase):
    def test_straight_line_has_no_corner(self):
        points = [[float(i), 0.0, 0.0] for i in range(20)]
        self.assertEqual(find_corners(points, window=4, min_angle_degrees=30.0), [])

    def test_right_angle_yields_one_corner(self):
        # L-shape: go along x, then turn 90 degrees to go along y.
        points = [[float(i), 0.0, 0.0] for i in range(10)] + \
                 [[9.0, float(j), 0.0] for j in range(1, 10)]
        corners = find_corners(points, window=3, min_angle_degrees=45.0)
        self.assertEqual(len(corners), 1)
        # The corner must sit at the bend around index 9.
        self.assertAlmostEqual(points[corners[0]][0], 9.0)
        self.assertAlmostEqual(points[corners[0]][1], 0.0)


class SegmentPathTests(unittest.TestCase):
    def test_straight_line_is_one_segment(self):
        points = [[float(i), 0.0, 0.0] for i in range(10)]
        segments = segment_path(points, window=3, min_angle_degrees=30.0)
        self.assertEqual(len(segments), 1)
        self.assertEqual(segments[0], points)

    def test_l_shape_splits_into_two_segments_sharing_corner(self):
        points = [[float(i), 0.0, 0.0] for i in range(10)] + \
                 [[9.0, float(j), 0.0] for j in range(1, 10)]
        segments = segment_path(points, window=3, min_angle_degrees=45.0)
        self.assertEqual(len(segments), 2)
        # The shared corner point must be the last of seg1 and the first of seg2.
        self.assertEqual(segments[0][-1], segments[1][0])


if __name__ == "__main__":
    unittest.main()
