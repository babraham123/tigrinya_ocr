#!/bin/bash
#Train tesseract!

usage() {
        echo "Usage: $0 <Number of files to train>"
        exit 1
}

[[ $# -eq 0 ]] && usage

for ((i=0;i<$1;i++))
do
	tesseract gez.geez.exp$i.tiff gez.geez.exp$i batch.nochop makebox
done
