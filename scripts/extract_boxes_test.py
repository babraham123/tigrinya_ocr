#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Tests for the bounding box logic.

import unittest
import extract_boxes as eb

class TestBoxManipulation(unittest.TestCase):
    def setUp(self):
        self.b1 = [1, 1, 5, 5]
        self.b2 = [6, 1, 10, 5]
        self.b3 = [10, 10, 11, 15]
        self.b4 = [10, 16, 11, 20]
        self.b5 = [-10, -10, 20, 20]

    def test_combine_box(self):
        # transitive
        self.assertListEqual(eb.combine_box(self.b1, self.b2), [1, 1, 10, 5])
        self.assertListEqual(eb.combine_box(self.b2, self.b1), [1, 1, 10, 5])

    def test_combine_boxes(self):
        old_min = eb._min_separation
        eb._min_separation = 5
        # identity
        self.assertListEqual(eb.combine_boxes([self.b2, self.b4]), [self.b2, self.b4])
        # horizontal
        self.assertListEqual(eb.combine_boxes([self.b1, self.b2, self.b3]), [[1, 1, 10, 5], self.b3])
        # vertical
        self.assertListEqual(eb.combine_boxes([self.b1, self.b3, self.b4]), [self.b1, [10, 10, 11, 20]])
        # both
        self.assertListEqual(eb.combine_boxes([self.b1, self.b2, self.b3, self.b4]), [[1, 1, 10, 5], [10, 10, 11, 20]])
        # internal
        self.assertListEqual(eb.combine_boxes([self.b1, self.b5]), [self.b5])
        self.assertListEqual(eb.combine_boxes([self.b5, self.b1]), [self.b5])
        eb._min_separation = old_min
 
    def test_convert_boxes(self):
        page = [0, 0, 0, 20]
        self.assertListEqual(eb.convert_boxes(page, [self.b1]), [[4, 76, 20, 60]])

if __name__ == '__main__':
    unittest.main()