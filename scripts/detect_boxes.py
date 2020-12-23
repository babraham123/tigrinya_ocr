#!/usr/bin/env python
# -*- coding: utf-8 -*-

# python script to detect text blocks in pdfs
# pip install pdfminer.six
# example:
#  python ./detect_boxes.py source.pdf output_dir
#
#  python ~/tigrinya_ocr/scripts/detect_boxes.py
#           ~/tigrinya_ocr/raw_data/Tigrigna-Grammar-i-vs-e.pdf
#           ~/segment/generated

from graphics import *
import os.path
import sys

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator

_pdf_resolution = 72
_png_resolution = 288
_min_separation = 7
_text_boxes = []

multiplier = 4
# minecart's native dpi is 72 for all coordinates
def_res = 72

_pdf_resolution = 72
_png_resolution = 288
_min_separation = 7
_text_boxes = []

def combine_box(box0, box1):
    return [min(box0[0], box1[0]), min(box0[1], box1[1]), max(box0[2], box1[2]), max(box0[3], box1[3])]

def combine_boxes(boxes):
    # Loop thru every unique pairing, i != j
    # check for close neighbors and overlaps.
    # PDF coordinates, origin in lower left
    i = 0
    j = 1
    num_b = len(boxes)
    while i < len(boxes):
        while j < len(boxes):
            msg = ''
            combine = False
            # First check alignment
            if abs(boxes[i][0] - boxes[j][0]) <= _min_separation and abs(boxes[i][2] - boxes[j][2]) <= _min_separation:
                # vertical closeness / overlap
                if (boxes[i][1] - _min_separation) <= boxes[j][3] and (boxes[i][3] + _min_separation) >= boxes[j][1]:
                    msg = 'v'
                    combine = True
            elif abs(boxes[i][1] - boxes[j][1]) <= _min_separation and abs(boxes[i][3] - boxes[j][3]) <= _min_separation:
                # horizontal closeness / overlap
                if (boxes[i][0] - _min_separation) <= boxes[j][2] and (boxes[i][2] + _min_separation) >= boxes[j][0]:
                    msg = 'h'
                    combine = True

            if combine:
                # print(msg, str(boxes[i]), '|', str(boxes[j]))
                boxes[i] = combine_box(boxes[i], boxes[j])
                del boxes[j]
                j = i

            j = j + 1
        i = i + 1
        j = i + 1

    print(num_b, '->', len(boxes), 'boxes,', num_b - len(boxes), 'combined')
    return boxes

def convert_boxes(page_size, boxes):
    ret_boxes = []
    multiplier = int(_png_resolution / _pdf_resolution)

    for box in boxes:
        # zero is lower left
        # obj.bbox from parse_obj
        box = [box[0], page_size[3] - box[1], box[2], page_size[3] - box[3]]
        box = [b * multiplier for b in box]
        ret_boxes.append(box)
    return ret_boxes

def parse_obj(lt_objs):
    global _text_boxes
    for obj in lt_objs:
        if isinstance(obj, pdfminer.layout.LTTextBoxHorizontal):
            # print('Box:' + str(obj.bbox) + '|' + str(bbox))
            _text_boxes.append(obj.bbox)

        elif isinstance(obj, pdfminer.layout.LTFigure):
            parse_obj(obj._objs)

def parse_document(filename):
    global _text_boxes

    fp = open(filename, 'rb')
    parser = PDFParser(fp)
    document = PDFDocument(parser)
    if not document.is_extractable:
        raise pdfminer.pdfpage.PDFTextExtractionNotAllowed

    # Create a PDF resource manager object that stores shared resources.
    rsrcmgr = PDFResourceManager()
    device = PDFDevice(rsrcmgr)

    # BEGIN LAYOUT ANALYSIS
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    # loop over all pages in the document
    boxes = []
    for page in PDFPage.create_pages(document):
        _text_boxes = []
        interpreter.process_page(page)
        layout = device.get_result()
        print('Page: ' + str(page.mediabox) + ' | ' + str(page.cropbox))
        page_size = page.mediabox
        parse_obj(layout._objs)

        page_boxes = _text_boxes.copy()
        # page_boxes = [[100, 100, 500, 500], [200, 600, 400, 800], [501, 100, 901, 501], [200, 805, 400, 905]]
        page_boxes = combine_boxes(page_boxes)
        page_boxes = convert_boxes(page_size, page_boxes)
        boxes.extend(page_boxes)

    _text_boxes = []
    return boxes

def draw_boxes(filename, boxes):
    img = matplotlib.image.imread(filename)
    figure, ax = plt.subplots(1)
    ax.imshow(img)
    for box in boxes:
        # zero is upper left
        # xy, width, -height (y inverted), angle
        rect = patches.Rectangle((box[0], box[1]), box[2] - box[0], box[3] - box[1], 0.0, edgecolor='r', facecolor="none")
        ax.add_patch(rect)
    plt.show()

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
