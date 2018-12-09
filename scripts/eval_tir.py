#!/usr/bin/env python
# -*- coding: utf-8 -*-

# python script to create and evaluate Tigrinya PDFs from the corpus

from evaluate import *

filename_in = '/home/babraham/tigrinya_ocr/eval/tir_corpus.txt'
# font_dir = '/Users/babraham/Library/Fonts/'
font_dir = '/home/babraham/tigrinya_ocr/fonts/'
langs = ['tir', 'amh']

fonts_by_level = {
    'easy': {
        'Abyssinica SIL': 'AbyssinicaSIL-R.ttf',
        'Abyssinica SIL Sebatbeit': 'AbyssinicaSIL-Sebatbeit-with-gwa.ttf',  # AbyssinicaSIL-Sebatbeit.ttf
        'Ethiopia Jiret': 'jiret.ttf',
        'Ethiopic Hiwua': 'hiwua.ttf',
        'Ethiopic Tint': 'tint.ttf',
        'Ethiopic WashRa Bold': 'washrab.ttf',
        'Ethiopic WashRa SemiBold': 'washrasb.ttf',
        'Ethiopic Yebse': 'yebse.ttf',
        'Ethiopic Zelan': 'zelan.ttf',
    },
    'medium': {
        'Code2003': 'Code200365k.ttf',
        'Ethiopic Fantuwua': 'fantuwua.ttf',
        'Ethiopic Wookianos': 'wookianos.ttf',
        'Ethiopic Yigezu Bisrat Goffer': 'goffer.ttf',
    },
    'hard': {
        'Abyssinica SIL Ximtanga': 'AbyssinicaSIL-R-designsource-20130811-Khimtanga.ttf',
        'Abyssinica SIL Zaima': 'AbyssinicaSIL-R-designsource-zaima-extensions.ttf',
        'Ethiopic Yigezu Bisrat Gothic': 'yigezubisratgothic.ttf',
        'GF Zemen Unicode': 'gfzemenu.ttf'
    },
}

def main():
    register_fonts(fonts_by_level, font_dir)

    # read corpus
    with open(filename_in) as f:
        text = f.readlines()
    text = [x[:-1].decode('utf-8') for x in text]
    filename = remove_ext(filename_in)

    # eval_sample(filename, text, 'Abyssinica SIL', 'tir')

    eval_all(filename, text, fonts_by_level, langs)


if __name__ == "__main__":
    main()
