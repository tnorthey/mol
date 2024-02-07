#!/bin/bash

step=$1  # 20, 30 40 50 etc

file=r05_dihedral_"$step".dat
rm $file
for i in ../tmp_/"$step"_1d_???.*.xyz
do
head -n 2 $i | tail -1 | awk '{print $3, $4;}' >> $file
done

