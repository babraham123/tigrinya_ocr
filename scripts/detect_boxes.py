#!/usr/bin/env python
# -*- coding: utf-8 -*-

# python script to detect text blocks in pdfs
# pip install minecart --user
# example:
#  python ~/tigrinya_ocr/scripts/detect_boxes.py source.pdf output_dir
#    ~/tigrinya_ocr/raw_data/Tigrigna-Grammar-i-vs-e.pdf
#    ~/segment/generated

from graphics import *
import minecart
import os.path
import sys

multiplier = 4
# minecart's native dpi is 72 for all coordinates
def_res = 72

def normalize_bbox(bbox, size):
    # left, bottom, right, top
    # width, height
    return [bbox[0]*multiplier, (size[1] - bbox[1])*multiplier, bbox[2]*multiplier, (size[1] - bbox[3])*multiplier]

def is_overlapped(box_a, box_b, x_tol = 0, y_tol = 0):
    # box = [x1, y1, x2, y2]
    box_a = [box_a[0] - x_tol, box_a[1] - y_tol, box_a[2] + x_tol, box_a[3] + y_tol]
    return box_a[2] >= box_b[0] and box_b[2] >= box_a[0] and box_a[3] >= box_b[1] and box_b[3] >= box_a[1]

def combine_bboxes(box_a, box_b):
    return [min(box_a[0], box_b[0]), min(box_a[1], box_b[1]), max(box_a[2], box_b[2]), max(box_a[3], box_b[3])]

def aggregate_bboxes(bboxes):
    new_bboxes = []
    bbox = bboxes[0]
    for i in range(len(bboxes) - 1):
        if is_overlapped(bbox, bboxes[i+1], x_tol = 10):
            bbox = combine_bboxes(bbox, bboxes[i+1])
        else:
            new_bboxes.append(bbox)
            bbox = bboxes[i+1]

    new_bboxes.append(bbox)
    return new_bboxes

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

    img_pages = pdf_to_png(pdf_name, output_path=output_dir, resolution=def_res*multiplier)
    print('Converted to png.')

    pdf_file = open(pdf_name, 'rb')
    doc = minecart.Document(pdf_file)
    # page = doc.get_page(0)
    fonts = {}
    for i, page in enumerate(doc.iter_pages()):
        size = [page.width, page.height]
        images = []
        shapes = []
        texts = []

        for image in page.images:
            # im = image.as_pil()  # requires pillow
            images.append(normalize_bbox(image.get_bbox(), size))

        for text in page.letterings:
            fonts[text.font] = 1
            texts.append(normalize_bbox(text.get_bbox(), size))

        for shape in page.shapes:
            # shape.path -> segments
            shapes.append(normalize_bbox(shape.get_bbox(), size))

        lines = aggregate_bboxes(texts)
        lines = aggregate_bboxes(lines)

        draw_boxes(img_pages[i], shapes, color='yellow')
        draw_boxes(img_pages[i], images, color='green')
        draw_boxes(img_pages[i], lines, color='red')
        print('Drew mined boxes for page %d.' % i)
    
    print(fonts.keys())
    print('Done!')


if __name__ == '__main__':
    main()
