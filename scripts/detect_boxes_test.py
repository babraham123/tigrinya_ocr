#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Tests for the bounding box logic.

import unittest
from detect_boxes import *

class TestBoxAggregation(unittest.TestCase):
    def setUp(self):
        self.b1 = [1, 1, 4, 2]
        self.b2 = [1, 1, 2, 4]
        self.b3 = [3, 3, 4, 4]
        self.b4 = [10, 1, 12, 2]

    def test_is_overlapped(self):
        self.assertTrue(is_overlapped(self.b1, self.b2))
        self.assertFalse(is_overlapped(self.b1, self.b3))
        self.assertFalse(is_overlapped(self.b2, self.b3))

    def test_is_overlapped_border(self):
        self.assertTrue(is_overlapped(self.b1, self.b2, x_tol=1, y_tol=1))
        self.assertFalse(is_overlapped(self.b1, self.b3, x_tol=1, y_tol=0))
        self.assertFalse(is_overlapped(self.b2, self.b3, x_tol=0, y_tol=1))
 
    def test_combine(self):
        bb = combine_n_bboxes([self.b1, self.b2])
        self.assertEqual(bb, [1, 1, 4, 4])
        self.assertTrue(is_overlapped(self.b3, bb))
        self.assertTrue(is_overlapped(self.b4, bb))

    def test_aggregate(self):
        # tol = 5
        bbs = aggregate_bboxes([self.b1, self.b2, self.b3, self.b4])
        self.assertEqual(bbs[0], self.b4)
        self.assertEqual(bbs[1], [1, 1, 4, 4])
        self.assertEqual(len(bbs), 2)

if __name__ == '__main__':
    unittest.main()