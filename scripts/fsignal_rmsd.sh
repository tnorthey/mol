#!/bin/bash

step=$1  # 20, 30 40 50 etc

file=fsignal_rmsd_"$step".dat
touch $file
rm $file 
for i in ../tmp_/"$step"_1d_???.*.xyz
do
head -n 2 $i | tail -1 | awk '{print $1, $2;}' >> $file
done

