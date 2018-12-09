#!/usr/bin/env python
# -*- coding: utf-8 -*-

# python script to create and evaluate English PDFs from the corpus

from evaluate import *

filename_in = '/home/babraham/tigrinya_ocr/eval/eng_corpus.txt'
font_dir = '/usr/share/fonts/truetype/msttcorefonts/'
langs = ['eng', 'spa', 'fra', 'deu']

fonts_by_level = {
    'easy': {
        'Arial': 'arial.ttf',
        'Georgia': 'georgia.ttf',
        'Times New Roman': 'times.ttf',
        'Trebuchet MS': 'trebuc.ttf',
        'Verdana': 'verdana.ttf',
    },
}

def main():
    register_fonts(fonts_by_level, font_dir)

    # read corpus
    with open(filename_in) as f:
        text = f.readlines()
    text = [x[:-1].decode('utf-8') for x in text]
    filename = remove_ext(filename_in)

    # eval_sample(filename, text, 'Arial', 'eng')

    eval_all(filename, text, fonts_by_level, langs)


if __name__ == "__main__":
    main()
