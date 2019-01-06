#!/bin/bash
# commands to train and run Calamari / Kraken OCR

# full pipeline with default params
kraken -i image.tif image.txt binarize segment ocr

# binarize a single image using the nlbin algorithm
kraken -i image.tif bw.png binarize

# segment a binarized image into reading-order sorted lines
kraken -i bw.png lines.json segment

# OCR a binarized image using the default RNN and the previously generated page segmentation
kraken -i bw.png image.txt ocr --lines lines.json

# train a kraken model

