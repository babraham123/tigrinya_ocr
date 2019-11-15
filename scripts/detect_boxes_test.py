#!/usr/bin/env python
# -*- coding: utf-8 -*-

from detect_boxes import *

def main():
  b1 = [1, 1, 4, 2]
  b2 = [1, 1, 2, 4]
  b3 = [3, 3, 4, 4]
  if not is_overlapped(b1, b2):
    print('b1 and b2 should overlap')

  if is_overlapped(b1, b3):
    print('b1 and b3 should not overlap')

  if is_overlapped(b2, b3):
    print('b2 and b3 should not overlap')

  b4 = combine_n_bboxes([b1, b2])
  print(b4)
  if not is_overlapped(b3, b4):
    print('b3 and b4 should overlap')

if __name__ == '__main__':
    main()

