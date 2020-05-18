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
    # origin is in the upper left corner
    # width, height
    return [bbox[0]*multiplier, (size[1] - bbox[1])*multiplier, bbox[2]*multiplier, (size[1] - bbox[3])*multiplier]

def is_overlapped(box_a, box_b, x_tol=0, y_tol=0):
    # box = [x1, y1, x2, y2]
    box_a = [box_a[0] - x_tol, box_a[1] + y_tol, box_a[2] + x_tol, box_a[3] - y_tol]
    return box_a[2] >= box_b[0] and box_a[0] <= box_b[2] and box_a[3] <= box_b[1] and box_a[1] >= box_b[3]

def combine_bboxes(box_a, box_b):
    return [min(box_a[0], box_b[0]), min(box_a[1], box_b[1]), max(box_a[2], box_b[2]), max(box_a[3], box_b[3])]

def combine_n_bboxes(bboxes):
    return [
        min(bboxes, key=lambda b: b[0])[0],
        min(bboxes, key=lambda b: b[1])[1],
        max(bboxes, key=lambda b: b[2])[2],
        max(bboxes, key=lambda b: b[3])[3]
    ]

def aggregate_bboxes(bboxes):
    # Finding overlapping pairs, find unions
    # left, bottom, right, top

    # overlapping pairs
    overlapping = {}
    overlapping_boxes = set()
    for i in range(len(bboxes) - 1):
        for j in range(i + 1, len(bboxes)):
            if is_overlapped(bboxes[i], bboxes[j], x_tol=5, y_tol=5):
                overlapping_boxes.add(i)
                overlapping_boxes.add(j)
                if i in overlapping:
                    overlapping[i].append(j)
                else:
                    overlapping[i] = [j]

    single_boxes = set(range(len(bboxes))) - overlapping_boxes

    # union of pairs
    for h in range(len(overlapping)):
        old_size = 0
        while old_size != len(overlapping[h]):
            n = old_size
            old_size = len(overlapping[h])
            for k in range(n, len(overlapping[h])):
                if overlapping[h][k] in overlapping:
                    overlapping[h].extend(overlapping[overlapping[h][k]])
                    overlapping[overlapping[h][k]] = []

    # dereference indices and combine into 1 list
    new_bboxes = [bboxes[i] for i in single_boxes]
    for g in overlapping:
        if overlapping[g]:
            indices = overlapping[g] + [g]
            bbox = combine_n_bboxes([bboxes[i] for i in indices])
            new_bboxes.append(bbox)
    return new_bboxes

def aggregate_bboxes_v2(bboxes):
    i = 0
    while i < len(bboxes):
        bbox = bboxes.pop(i)
        for j in range(len(bboxes) - 1, -1, -1):
            if is_overlapped(bbox, bboxes[j], x_tol = 10):
                bbox = combine_bboxes(bbox, bboxes.pop(j))
                if j <= i:
                    i = i - 1

        bboxes.insert(0, bbox)
        i = i + 1

    return bboxes

def main():
    if len(sys.argv) < 2:
        print('Incorrect # of arguments!')
        exit(1)
    pdf_name = sys.argv[1]
    if len(sys.argv) < 3:
        output_dir = '.'
    else:
        output_dir = sys.argv[2]
    if not os.path.exists(pdf_name) or not os.path.exists(output_dir):
        print('File/dir does not exist!')
        exit(1)
    (path, ext) = os.path.splitext(pdf_name)
    if ext.lower() != '.pdf':
        print('File is not a pdf!')
        exit(1)

    img_pages = pdf_to_png(pdf_name, output_path=output_dir, resolution=def_res*multiplier)
    print('Converted to png.')

    pdf_file = open(pdf_name, 'rb')
    doc = minecart.Document(pdf_file)
    # page = doc.get_page(0)
    fonts = {}
    for i, page in enumerate(doc.iter_pages()):
        size = [page.width, page.height]
        print('Page size %s' % str(size))
        images = []
        shapes = []
        texts = []

        for image in page.images:
            # im = image.as_pil()  # requires pillow
            images.append(normalize_bbox(image.get_bbox(), size))

        for text in page.letterings:
            fonts[text.font] = 1
            texts.append(normalize_bbox(text.get_bbox(), size))
            texts_raw = text.get_bbox()
        print(texts_raw[0:10])

        for shape in page.shapes:
            # shape.path -> segments
            shapes.append(normalize_bbox(shape.get_bbox(), size))

        print('%d text segments' % len(texts))
        # lines = aggregate_bboxes(texts)
        # print('%d lines of text' % len(lines))

        draw_boxes(img_pages[i], shapes, color='yellow')
        draw_boxes(img_pages[i], images, color='green')
        draw_boxes(img_pages[i], texts[0:10], color='red')
        print('Drew mined boxes for page %d.' % i)
        print(texts[0:10])
    
    print(fonts.keys())
    print('Done!')


if __name__ == '__main__':
    main()
