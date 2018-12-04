#!/usr/bin/env python
# -*- coding: utf-8 -*-

# python script to create and evaluate English PDFs from the corpus

from evaluate import *

filename_in = '../raw_data/eng_corpus.txt'
# font_dir = '/Users/babraham/Library/Fonts/'
font_dir = ''
langs = ['eng', 'spa', 'fra', 'deu']
lines_per_page = 25

fonts = {
    'easy': [
        'Arial',
        'Garamond',
        'Times New Roman',
        'Trebuchet MS',
        'Courier New',
    ],
}

def main():
    # read corpus
    with open(filename_in) as f:
        text = f.readlines()
    text = [x.decode('utf-8') for x in text]
    filename = remove_ext(filename_in)

    pdf_file = create_pdf(filename, text, 'Arial')
    img_file = pdf_to_tif(remove_ext(pdf_file))
    print_ocr(img_file, 'eng')
    print('\n')

    eval_all(filename, text, fonts_by_level, langs)


if __name__ == "__main__":
    main()
