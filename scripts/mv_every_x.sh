#!/bin/bash
# sh mv_every_x.sh eval_1/ 10

n=0
for file in ./*.*; do
   test $n -eq 0 && mv "$file" $1
   n=$((n+1))
   n=$((n%$2))
done
