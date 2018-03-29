#!/bin/bash
#Run all Tesseract scripts!

usage() {
        echo "Usage: $0 <PDF File to split>"
        exit 1
}

[[ $# -eq 0 ]] && usage

find . -name '*.txt' -delete
find . -name '*.tiff' -delete
find . -name '*.box' -delete
find . -name '*.tr' -delete
find . -name "*exp*.pdf" | xargs rm
./build.sh $1
a=`find . -name "*exp*.pdf" | wc -l`
./adjust.sh $a
./convert.sh $a
./train.sh $a
