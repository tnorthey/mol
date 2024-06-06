#!/bin/bash

filename=$1
nlines=$(cat $filename | wc -l)
#echo "nlines: "$nlines""
low_quartile=$((nlines / 4))
#echo "low quartile: "$low_quartile""

avg_low_quartile=$(awk '{print $5}' $filename | head -n $low_quartile | awk -v var="$low_quartile" '{SUM+=$1};END{printf "%.8g\n", SUM/var}')
echo $avg_low_quartile

