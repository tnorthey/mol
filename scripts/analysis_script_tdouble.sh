#!/bin/bash

path=$1  # e.g. ../results_/
description=$2  # append a description to the .dat files

#for step in 10 20 30 35 40 50 60
#for step in 10 20 30 40 50 60 70 75
#for step in 10 20 32 35 37 40 44 50 55 60 65 70 75
#for step in 20 32 35 37 40 44 50 55 60 65 70
#for step in 20 35 40 45 50 55 60 65 70 75
for step in {0..9}
do
	file1=analysis_"$step"_"$description".dat
	touch $file1 $file2
	rm $file1 $file2
	for i in $path/"$step"_1d_???.*.xyz
	do
		head -n 2 $i | tail -1 | awk '{print $3, $4, $5, $1, $2, $6, $7;}' >> $file1
	done
done

