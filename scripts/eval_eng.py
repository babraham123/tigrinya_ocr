#!/usr/bin/env python
# -*- coding: utf-8 -*-

# python script to create and evaluate English PDFs from the corpus

from evaluate import *

filename_in = '/home/babraham/tigrinya_ocr/eval/eng_corpus.txt'
langs = ['eng', 'spa', 'fra', 'deu']

fonts = {
    'easy': {
        'Arial': 'arial.ttf',
        'Georgia': 'georgia.ttf',
        'Times New Roman': 'times.ttf',
        'Trebuchet MS': 'trebuc.ttf',
        'Verdana': 'verdana.ttf',
    },
}

def main():
    # register all fonts
    for level, fonts in fonts_by_level:
        for font_name, font_file in fonts:
            pdfmetrics.registerFont(TTFont(font_name, font_dir + font_file))

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
