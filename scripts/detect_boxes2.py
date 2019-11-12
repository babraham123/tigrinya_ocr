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
def normalize_bbox(bbox):
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

    pdf_file = open(pdf_name, 'rb')
    doc = minecart.Document(pdf_file)
    # page = doc.get_page(0)
    fonts = {}
    for i, page in enumerate(doc.iter_pages()):
        images = []
        shapes = []
        texts = []

        for image in page.images:
            # im = image.as_pil()  # requires pillow
            images.append(normalize_bbox(image.get_bbox()))

        for text in page.letterings:
            fonts[text.font] = 1
            texts.append(normalize_bbox(text.get_bbox()))

        for shape in page.shapes:
            # shape.path -> segments
            shapes.append(normalize_bbox(shape.get_bbox()))

        draw_boxes(img_pages[i], shapes, color='yellow')
        draw_boxes(img_pages[i], images, color='green')
        draw_boxes(img_pages[i], texts, color='red')
        print('Drew mined boxes for page %d.' % i)
    
    print(fonts.keys())
    print('Done!')


if __name__ == '__main__':
    main()
