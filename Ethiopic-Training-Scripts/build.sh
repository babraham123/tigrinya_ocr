#!/bin/bash
#Build the file from an input pdf
usage() {
	echo "Usage: $0 <PDF File to split>"
	exit 1
}
	
[[ $# -eq 0 ]] && usage

pdftk $1 burst output gez.geez.exp%d.pdf 
