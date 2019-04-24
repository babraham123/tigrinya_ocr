#!/usr/bin/env python
# -*- coding: utf-8 -*-

# python script to convert pdfs into segmentable pngs
# sudo apt-get install libreoffice

from graphics import *
import os, sys, glob, subprocess

dpi_ = 100 # pixels per inch
max_length_ = 11 * dpi_  # inches
# typical page is 8.5 x 11in
max_pages_ = 15


def main():
    if len(sys.argv) != 3:
        print('Incorrect arguments!')
        exit()

    pdf_dir = sys.argv[1]
    image_dir = sys.argv[2]
    if not os.path.isdir(image_dir) or not os.path.isdir(pdf_dir):
        print('Folder(s) do not exist!')
        exit()

    # walk thru pdf directory
    print('conversion...')
    num_inputs = 0
    for root, dirs, files in os.walk(pdf_dir):
        for filename in files:
            file = os.path.join(root, filename)
            if not os.path.isfile(file):
                continue
            num_inputs += 1
            result = convert_to_png(file, image_dir, max_pages_, dpi_)
            print(result)

    # binarize pngs
    print('slice and binarize...')
    final_imgs = []
    for file in glob.glob(os.path.join(image_dir, '*.png')):
        result = slice_img(file, max_length_, 0.2)
        print(result)
        if not result:
            result = [file]

        if file not in result:
            os.remove(file)

        for part_file in result:
            try:
                subprocess.run(['kraken', '-i', part_file, part_file, 'binarize'], check=True) # shell=True
                final_imgs.append(part_file)
            except Exception as ex:
                print(ex)
    print(str(len(final_imgs)) + ' out of ' + str(num_inputs) + ' files converted.')

if __name__ == '__main__':
    main()
