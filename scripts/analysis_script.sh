#!/bin/bash

path=$1  # e.g. ../results_/
step=$2  # 20, 30 40 50 etc
description=$3  # append a description to the .dat files

file1=r05_dihedral_"$step"_"$description".dat
file2=rmsd_fsignal_"$step"_"$description".dat
touch $file1 $file2
rm $file1 $file2
for i in $path/"$step"_1d_???.*.xyz
do
head -n 2 $i | tail -1 | awk '{print $3, $4;}' >> $file1
head -n 2 $i | tail -1 | awk '{print $2, $1;}' >> $file2
done

