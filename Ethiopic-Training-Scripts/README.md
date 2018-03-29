Tesseract Trainer Program
=========================

Introduction
------------
This program and set of bash scripts was designed as a supplement to research done by Travis Cramer and Elizabeth Carlisle, supervised by James Prather

Dependencies
------------
You must have ImageMagick installed and on your path, as well as have all Tesseract executable files on your path. To automate the splitting procedure, I have used PDFtk, which is a free installation from http://www.pdflabs.com/tools/pdftk-server/

Make sure it all of these are on the path and executing before running the scripts!

Usage
-----
To run on some PDF, run run.sh with the PDF file as a parameter. 

EX: './run.sh tesseract_test.pdf'

Files
-----
run.sh: The master script that runs the training procedure up to box file creation.
adjust.sh: Adjusts the file names outputted from build.sh
build.sh: Splits an input PDF file into paginated files
convert.sh: Uses ImageMagick to convert 
train.sh: Runs the pre-box training commands
posttrain.sh: Runs all post-box commands

TODO
----
Check TODO file for more info
