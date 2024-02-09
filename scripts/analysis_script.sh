#!/bin/bash

path=$1  # e.g. ../results_/
description=$2  # append a description to the .dat files

for step in 10 20 30 35 40 50 60
do
	file1=r05_dihedral_"$step"_"$description".dat
	file2=rmsd_fsignal_"$step"_"$description".dat
	touch $file1 $file2
	rm $file1 $file2
	for i in $path/"$step"_1d_???.*.xyz
	do
		head -n 2 $i | tail -1 | awk '{print $3, $4;}' >> $file1
		head -n 2 $i | tail -1 | awk '{print $2, $1;}' >> $file2
	done
done

