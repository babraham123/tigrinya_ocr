#!/bin/bash
# commands to train and run Calamari / Kraken OCR

# full pipeline with default params
kraken -i image.tif image.txt binarize segment ocr

# binarize a single image using the nlbin algorithm
kraken -i image.tif bw.png binarize

# segment a binarized image into reading-order sorted lines, with script detection
kraken -i bw.png lines.json segment -s

kraken list
kraken get default
ls ~/.config/kraken/

# OCR a binarized image using the default RNN and the previously generated page segmentation
kraken -i bw.png image.txt ocr --lines lines.json

# create a corpus, wrap words
cat *.txt > corpus.txt
python scripts/word_wrap.py

# generate synthetic data
ketos linegen -u NFD -f "Abyssinica SIL" corpus.txt

# predict with voting mechanism
calamari-predict --checkpoint 0.ckpt --checkpoint 1.ckpt --files *.png

# evaluate predictions
calamari-eval --gt *.gt.txt

# train a calamari model
calamari-cross-fold-train --files training_data/*.png --best_models_dir models --temporary_dir tmp &> training.log


