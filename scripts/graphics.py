#!/usr/bin/env python
# -*- coding: utf-8 -*-

# python lib to handle drawing and file conversion tasks.
# ref: http://docs.wand-py.org/en/0.5.0/guide/draw.html

import glob, json, os, random, subprocess, re
from wand.image import Image
from wand.color import Color
from wand.drawing import Drawing
from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger


def convert_to_png(filename, output_path, max_pages=None, resolution=300):
    """ Converts a number of file formats into png images.

        Supports pdf, doc, jpg, tif, txt(?).
    """
    (name, ext) = os.path.splitext(filename)
    ext = ext.lower()
    ret = None
    if ext == '.pdf':
        ret = pdf_to_png(filename, output_path=output_path, max_pages=max_pages, resolution=resolution)
        # print('Converted: ', filename)
    elif ext in ['.png', '.jpg', '.jpeg', '.tif', '.tiff']:
        ret = img_to_png(filename, output_path=output_path, resolution=resolution)
        # print('Converted: ', filename)
    elif ext in ['.doc', '.docx', '.txt']:
        pdf = doc_to_pdf(filename, output_path=output_path)
        ret = pdf_to_png(pdf, output_path=output_path, max_pages=max_pages, resolution=resolution)
        os.remove(pdf)
    else:
        print('unknown file type: ', filename)
    return ret


def pdf_to_png(filename, output_path='.', max_pages=None, resolution=300):
    """ Convert a PDF into png images.

        All the pages will give a single png file with format:
        {pdf_filename}-{page_number}.png

        The function removes the alpha channel from the image and
        replace it with a white background.
    """
    all_pages = Image(filename=filename, resolution=resolution)
    num_pages = len(all_pages.sequence)
    num_digits = len(str(num_pages))
    base_name = os.path.splitext(os.path.basename(filename))[0]

    ret = []
    selected = []
    if not max_pages or num_pages <= max_pages:
        selected = [i for i in range(num_pages)]
    else:
        inc = num_pages // max_pages
        selected = [i for i in range(0, num_pages, inc)]

    # for i, page in enumerate(all_pages.sequence):
    for i in selected:
        with Image(all_pages.sequence[i]) as img:
            img.format = 'png'
            img.background_color = Color('white')
            img.alpha_channel = 'remove'
            image_filename = base_name
            image_filename = image_filename.replace(' ', '_')
            image_filename = '{}-{}.png'.format(image_filename, str(i).zfill(num_digits))
            image_filename = os.path.join(output_path, image_filename)
            img.save(filename=image_filename)
            ret.append(image_filename)
    return ret


def img_to_png(filename, output_path='.', resolution=300):
    """ Convert any supported image format into png.

        The function removes the alpha channel from the image and
        replace it with a white background.
    """
    image_filename = ''
    base_name = os.path.splitext(os.path.basename(filename))[0]

    with Image(filename=filename, resolution=resolution) as img:
        img.format = 'png'
        img.background_color = Color('white')
        img.alpha_channel = 'remove'
        image_filename = base_name
        image_filename = image_filename.replace(' ', '_')
        image_filename = os.path.join(output_path, image_filename)
        img.save(filename=image_filename)
    return [image_filename]


def slice_img(filename, max_length, overlap_ratio):
    """ Convert any supported image format into png.

        All the pages will give a single png file with format:
        {pdf_filename}-{page_number}.png

        The function removes the alpha channel from the image and
        replace it with a white background.
    """
    non_overlap = max_length * (1 - overlap_ratio)
    overlap = max_length * overlap_ratio
    (path, file) = os.path.split(filename)
    (name, ext) = os.path.splitext(file)
    assert(ext == '.png')
    ret = []

    with Image(filename=filename) as img:
        (width, height) = img.size
        if height <= max_length:
            return None

        parts = [i for i in range(0, height, non_overlap)]
        for i, part_y0 in enumerate(parts):
            if (height - part_y0) <= overlap:
                continue
            part_y1 = min(height, part_y0 + max_length)
            # [left:right, top:bottom]
            with img[:, part_y0:part_y1] as cropped:
                image_filename = '{}-{}.png'.format(name, chr(ord('a') + i))
                image_filename = os.path.join(path, image_filename)
                cropped.save(filename=image_filename)
                ret.append(image_filename)
    return ret


def doc_to_pdf(folder, source, timeout=None):
    args = ['libreoffice', '--headless', '--convert-to', 'pdf', '--outdir', folder, source]
    try:
        process = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
        filename = re.search('-> (.*?) using filter', process.stdout.decode())
    except Exception as ex:
        print(ex)
        return None

    if filename is None:
        print(process.stdout.decode())
        return None
    else:
        return filename.group(1)


def doc_to_pdf2(filename, output_path='.'):
    args = ['libreoffice', '--headless', '--convert-to', 'pdf', '--outdir', output_path, filename]
    base_name = os.path.splitext(os.path.basename(filename))[0]
    try:
        subprocess.run(args, check=True) # shell=True
        return os.path.join(output_path, base_name + '.pdf')
    except Exception as ex:
        print(ex)
        return None


def should_use(i, page_min, page_percent):
    """ Algorithm to randomly pick pages from a pdf to convert.
        Picks Y percent of pages after the first X is reached.
    """
    if i < page_min:
        return True
    p = random.random()
    return p < (page_percent / 100.0)


def remove_ext(filename):
    parts = filename.split('.')
    if len(parts) < 2:
        return filename, ''
    return '.'.join(parts[:-1])


def pdf_splitter(path):
    fname = os.path.splitext(path)[0]
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

