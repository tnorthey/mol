#!/bin/bash

starting_xyz_file=$1	# starting xyz filename
step=$2			# define the target frame e.g. 20, 30, 40, 50
run_id=""$step"_1d"	# run ID
target_xyz_file="xyz/target_traj094/target_$step.xyz"  # target xyz filename

echo "go script: starting_xyz_file $starting_xyz_file"
echo "go script: target_xyz_file $target_xyz_file"

python3 run_1D_chd.py $run_id $starting_xyz_file $target_xyz_file

#bestxyz=$(ls -1 tmp_/"$run_id"_???.????????.xyz | head -n 1) 
#bestdat=$(ls -1 tmp_/"$run_id"_???.????????.dat | head -n 1) 
#cp $bestxyz tmp_/"$run_id"_best.xyz
#cp $bestdat tmp_/"$run_id"_best.dat
