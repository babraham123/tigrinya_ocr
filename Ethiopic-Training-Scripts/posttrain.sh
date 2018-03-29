#!/bin/bash
#Run all post-box file Tesseract scripts!

a='find . -name "*exp*.pdf" | wc -l'

for ((i=0;i<$a;i++))
do
	tesseract gez.geez.exp0.tif gez.geez.box nobatch box.train.stderr
done

unicharset_extractor *.box
mftraining -F font_properties -U unicharset -O gez.unicharset *.tr
cntraining *.tr
combine_tessdata gez.
cp gez.traineddata /usr/local/share/tessdata/
