#!/bin/bash
# "${filename%.*}"

for j in 090 094 099
do

    path="xyz/target_traj$j"
    
    # this creates files target_??.dat in $path
    for i in $path/target_??.xyz; do 
        echo $i 
        python3 iam_wrapper.py $i
        mv iam_total.dat "${i%.*}".dat
    done
    
    # combine all target_??.dat files into one
    # 1. print only the second column
    for i in $path/target_??.dat; do
       awk '{print $2}' $i > tmp
       mv tmp $i
    done
    # 2. paste them all together
    paste $path/target_??.dat > $path/combined_iam_file.dat
    
    # clean unwanted files
    rm $path/target_??.dat
    rm iam_molecular.dat iam_compton.dat iam_atomic.dat

done
