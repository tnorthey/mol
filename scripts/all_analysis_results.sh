#!/bin/bash
### create .dat files from the xyz headers for plotting ###
### Change the path loop target to analyse different results directories

#for i in ../results_/results_noise*_qmax?_nrestarts5_traj09?_d23/
for path in ../results_/results_noise*_qmax?_nrestarts5_traj09?_low_constraints_c3/
do
    base_name=$(basename ${path})
    echo $base_name

    for step in 10 20 32 35 37 40 45 50 55 60 65 70 75
    do
	file1=analysis_"$step"_"$base_name".dat
	touch $file1 $file2; rm $file1 $file2

	for xyzfile in $path/"$step"_1d_???.*.xyz
	do
	    head -n 2 $xyzfile | tail -1 | awk '{print $3, $4, $5, $1, $2, $6, $7;}' >> $file1
	done
    done
done

