#!/bin/bash

path=$1  # e.g. ../results_/
step=$2  # 20, 30 40 50 etc

file1=r05_dihedral_"$step".dat
file2=fsignal_rmsd_"$step".dat
touch $file1 $file2
rm $file1 $file2
for i in $path/"$step"_1d_???.*.xyz
do
head -n 2 $i | tail -1 | awk '{print $3, $4;}' >> $file1
head -n 2 $i | tail -1 | awk '{print $1, $2;}' >> $file2
done

