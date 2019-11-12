#!/usr/bin/env python
# -*- coding: utf-8 -*-

# python script to detect text blocks in pdfs
# pip install pdfplumber --user
# example:
#  python ~/tigrinya_ocr/scripts/detect_boxes.py source.pdf output_dir
#    ~/tigrinya_ocr/raw_data/Tigrigna-Grammar-i-vs-e.pdf
#    ~/segment/generated

from graphics import *
import pdfplumber
import os.path
import sys

multiplier = 4

# pdfplumber's native dpi is 72 for all coordinates
def normalize_bbox(bbox, size):
    # left, bottom, right, top
    return [bbox[0]*multiplier, bbox[1]*multiplier, bbox[2]*multiplier, bbox[3]*multiplier]

def main():
    if len(sys.argv) < 2:
        print('Incorrect arguments!')
        exit()
    pdf_name = sys.argv[1]
    if len(sys.argv) < 3:
        output_dir = '.'
    else:
        output_dir = sys.argv[2]
    
    if not os.path.exists(pdf_name) or not os.path.exists(output_dir):
        print('File/dir do not exist!')
        exit()

    (path, ext) = os.path.splitext(pdf_name)
    if ext.lower() != '.pdf':
        print('File is not a pdf!')
        exit()

    img_pages = pdf_to_png(pdf_name, output_path=output_dir, resolution=72*multiplier)
    print('Converted to png.')

    pdf = pdfplumber.open(pdf_name)
    print(pdf.metadata)
    fonts = {}
    for page in pdf.pages:
        i = page.page_number - 1
        size = [page.width, page.height]

        lines = []
        shapes = []
        for text in page.lines:
            bbox = [text.x0, text.y0, text.x1, text.y1]
            lines.append(normalize_bbox(bbox, size))

        for obj in page.rects:
            bbox = [obj.x0, obj.y0, obj.x1, obj.y1]
            shapes.append(normalize_bbox(bbox, size))
        for obj in page.curves:
            bbox = [obj.x0, obj.y0, obj.x1, obj.y1]
            shapes.append(normalize_bbox(bbox, size))

        draw_boxes(img_pages[i], shapes, color='yellow')
        draw_boxes(img_pages[i], lines, color='red')
        print('Drew mined boxes for page %d.' % i)

    print('Done!')


if __name__ == '__main__':
    main()
