#!/usr/bin/env python
# -*- coding: utf-8 -*-

# python script to create and evaluate English PDFs from the corpus

from evaluate import *

filename_in = '/home/babraham/tigrinya_ocr/eval/eng_corpus.txt'
fontfile = '/usr/share/fonts/truetype/msttcorefonts/arial.ttf'
font = 'Arial'

def main():
    # register all fonts
    pdfmetrics.registerFont(TTFont(font, fontfile))

    # read corpus
    with open(filename_in) as f:
        text = f.readlines()
    text = [x.decode('utf-8') for x in text]

    eval_sample(remove_ext(filename_in), text, font, 'eng')


if __name__ == "__main__":
    main()
