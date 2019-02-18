#!/usr/bin/env python
# -*- coding: utf-8 -*-

# python script to draw bounding boxes

from graphics import *
import os.path
import sys


def main():
    image_file = sys.argv[1]
    box_file = sys.argv[2]

    if len(sys.argv) != 3:
        print('Incorrect arguments!')
        exit()
    if not os.path.exists(image_file) or not os.path.exists(box_file):
        print('File(s) do not exist!')
        exit()

    (path, ext) = os.path.splitext(image_file)
    if ext.lower() == '.pdf':
        pdf_to_png(image_file)
        image_file = path + '.png'
        print('Converted pdf to png...')

    boxes = read_kraken_bboxes(box_file)
    draw_boxes(image_file, boxes)
    print('Drew kraken boxes...')


if __name__ == "__main__":
    main()
