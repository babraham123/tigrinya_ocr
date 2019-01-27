#!/usr/bin/env python
# -*- coding: utf-8 -*-

# python script to draw bounding boxes

from graphics import *
import os.path

filename_1 = 'TIGRINA SUN 9 APR 2017.pdf'
filename_2 = 'TIGRINA_SUN_9_APR_2017-0.png'
filename_3 = 'lines.json'
filename_4 = 'bw.png'


def main():
    if not os.path.exists(filename_2):
        pdf_to_png(filename_1)
        print('Converted pdf to png...')

    if os.path.exists(filename_3):
        boxes = read_kraken_bboxes(filename_3)
        draw_boxes(filename_4, boxes)
        print('Drew kraken boxes...')

    

if __name__ == "__main__":
    main()
