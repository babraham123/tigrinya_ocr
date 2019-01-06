#!/usr/bin/env python
# -*- coding: utf-8 -*-

# python script to create images of text from the corpus

from evaluate import *
import os

test_pages = [{
    'filename': '/home/babraham/tigrinya_ocr/eval/eng_corpus.txt',
    'fontfile': '/usr/share/fonts/truetype/msttcorefonts/arial.ttf',
    'font': 'Arial',
    'lang': 'eng'
},
{
    'filename': '/home/babraham/tigrinya_ocr/eval/tir_corpus.txt',
    'fontfile': '/home/babraham/tigrinya_ocr/fonts/AbyssinicaSIL-R.ttf',
    'font': 'Abyssinica SIL',
    'lang': 'tir'
}]

def main():
    fonts = {page['font']: page['fontfile'] for page in test_pages}
    fonts_by_level = {'easy': fonts}
    register_fonts(fonts_by_level)

    for page in test_pages:
        # read corpus
        with open(page['filename']) as f:
            text = f.readlines()
        text = [x.decode('utf-8') for x in text[:25]]
        filename = remove_ext(page['filename'])

        # create page
        pdf_file = create_pdf(filename, text, page['font'])
        img_file = pdf_to_tif(remove_ext(pdf_file))
        os.remove(pdf_file)


if __name__ == "__main__":
    main()
