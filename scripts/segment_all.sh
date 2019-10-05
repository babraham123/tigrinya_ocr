#!/bin/bash
# sh segment_all.sh images/ labels/

for f in "${1}*.png"
do
   kraken -i "${f}" "${2}${f}.json" segment
done
