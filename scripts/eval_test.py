#!/usr/bin/env python
# -*- coding: utf-8 -*-

# python script to create and evaluate English PDFs from the corpus

from evaluate import *

filename_in = '/home/babraham/tigrinya_ocr/eval/eng_corpus.txt'
fontfile = '/usr/share/fonts/truetype/msttcorefonts/arial.ttf'
font = 'Arial'
fonts_by_level = {'easy': {font: fontfile}}
langs = ['eng']

def main():
    register_fonts(fonts_by_level)

    # read corpus
    with open(filename_in) as f:
        text = f.readlines()
    text = [x[:-1].decode('utf-8') for x in text[:25]]
    filename = remove_ext(filename_in)

    # eval_sample(filename, text, font, langs[0])

    eval_all(filename, text, fonts_by_level, langs, False)


if __name__ == "__main__":
    main()
