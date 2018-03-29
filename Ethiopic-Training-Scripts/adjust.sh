#!/bin/bash
#Adjust tesseract training files
usage(){
	echo "Usage: $0 <number of files"
	exit 1
}

[[ $# -eq 0 ]] && usage

for ((i=1;i<=$1;i++))
do
    mv "gez.geez.exp${i}.pdf" "gez.geez.exp$((i-1)).pdf"
done
