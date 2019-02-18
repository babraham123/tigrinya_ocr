#!/usr/bin/env python
# -*- coding: utf-8 -*-

# python lib to handle drawing and file conversion tasks.
# ref: http://docs.wand-py.org/en/0.5.0/guide/draw.html

import glob
import json
import os
from wand.image import Image
from wand.color import Color
from wand.drawing import Drawing
from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger

filename_ = 'TIGRINA SUN 9 APR 2017.pdf'


def pdf_to_png(filename, output_path='.', resolution=300):
    """ Convert a PDF into images.

        All the pages will give a single png file with format:
        {pdf_filename}-{page_number}.png

        The function removes the alpha channel from the image and
        replace it with a white background.
    """
    all_pages = Image(filename=filename, resolution=resolution)
    num_digits = len(str(len(all_pages.sequence)))
    for i, page in enumerate(all_pages.sequence):
        with Image(page) as img:
            img.format = 'png'
            img.background_color = Color('white')
            img.alpha_channel = 'remove'
            image_filename = os.path.splitext(os.path.basename(filename))[0]
            image_filename = image_filename.replace(' ', '_')
            image_filename = '{}-{}.png'.format(image_filename, str(i).zfill(num_digits))
            image_filename = os.path.join(output_path, image_filename)
            img.save(filename=image_filename)


def remove_ext(filename):
    parts = filename.split('.')
    if len(parts) < 2:
        return filename, ''
    return '.'.join(parts[:-1])


def pdf_splitter(path):
    fname = remove_ext(path)
    pdf = PdfFileReader(path)
    num_digits = len(str(pdf.getNumPages()))

    for page in range(pdf.getNumPages()):
        pdf_writer = PdfFileWriter()
        pdf_writer.addPage(pdf.getPage(page))
 
        output_filename = '{}_{}.pdf'.format(
            fname, str(page + 1).zfill(num_digits))

        with open(output_filename, 'wb') as out:
            pdf_writer.write(out)
 
    print('Split {} pages'.format(pdf.getNumPages()))


def pdf_merger(fname):
    paths = glob.glob(fname + '_*.pdf')
    paths.sort()

    pdf_merger = PdfFileMerger()
    output_path = fname + '.pdf'
 
    for path in paths:
        pdf_merger.append(path)
 
    with open(output_path, 'wb') as fileobj:
        pdf_merger.write(fileobj)

    print('Merged {} pages'.format(len(paths)))


def read_kraken_bboxes(filename):
    data = {}
    with open(filename) as json_file:  
        data = json.load(json_file)

    if 'boxes' not in data:
        if isinstance(data, list):
            return data
        else:
            return []

    if not isinstance(data['boxes'][0][0], list):
        return data['boxes']

    boxes = []
    for line in data['boxes']:
        for lang_group in line:
            # x1,y1 , x2,y2
            boxes.append(lang_group[1])
    return boxes


def draw_boxes(filename, boxes):
    with Drawing() as draw:
        draw.stroke_width = 2
        draw.stroke_color = Color('red')
        draw.fill_color = Color('white')
        draw.fill_opacity = 0
        for box in boxes:
            draw.polygon([(box[0], box[1]), (box[2], box[1]), (box[2], box[3]), (box[0], box[3])])
        # with Image(width=100, height=100, background=Color('lightblue')) as image:
        with Image(filename=filename) as image:
            draw(image)
            image.save(filename=filename)

