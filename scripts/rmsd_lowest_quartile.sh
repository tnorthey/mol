#!/bin/bash

# example run command:
# ./rmsd_lowest_quartile.sh 4.0 8 094

noise=$1
qmax=$2
traj=$3
ending=$4

#filename=$1
rmsd_tmp_file="rmsd_values.dat"
fxray_tmp_file="fxray_values.dat"

rm $rmsd_tmp_file || true
rm $fxray_tmp_file || true

#for filename in analysis_??_results_noise"$noise"_qmax"$qmax"_nrestarts5_traj"$traj".dat
#for step in 10 20
for step in 10 20 32 35 37 40 45 50 55 60 65 70 75
do
    filename=analysis_"$step"_results_noise"$noise"_qmax"$qmax"_nrestarts5_traj"$traj"_"$ending".dat
    #echo $filename
    nlines=$(cat $filename | wc -l)
    #echo "nlines: "$nlines""
    low_quartile=$((nlines / 4))
    #echo "low quartile: "$low_quartile""
    
    avg_rmsd_low_quartile=$(awk '{print $5}' $filename | head -n $low_quartile | awk -v var="$low_quartile" '{SUM+=$1};END{printf "%10.8f\n", SUM/var}')
    avg_fxray_low_quartile=$(awk '{print $4}' $filename | head -n $low_quartile | awk -v var="$low_quartile" '{SUM+=$1};END{printf "%10.8f\n", SUM/var}')
    echo $avg_rmsd_low_quartile >> $rmsd_tmp_file
    echo $avg_fxray_low_quartile >> $fxray_tmp_file
done

#awk '{n++;sum+=$1} END {printf "%.8g\n", n?sum/n:0}' values
str1=$(awk -v var=$noise '{n++;sum+=$1} END {printf "%2.1f %10.8f\n", var, n?sum/n:0}' $rmsd_tmp_file)
str2=$(awk '{n++;sum+=$1} END {printf "%10.8f\n", n?sum/n:0}' $fxray_tmp_file)
echo "$str1 $str2"
