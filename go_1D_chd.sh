#!/bin/bash

#starting_xyz_file="tmp_/$(($step-10))_1d_near.xyz"
starting_xyz_file=$1
step=$2  # define the target frame e.g. 20, 30, 40, 50
ringclosed=$3  # "closed" or "open"
run_id=""$step"_1d"
#target_xyz_file="xyz/target_traj099/target_$step.xyz"  # ring-open
target_xyz_file="xyz/target_traj094/target_$step.xyz"  # ring-open
python3 run_1D_chd.py $run_id $starting_xyz_file $target_xyz_file $ringclosed

bestxyz=$(ls -1 tmp_/"$step"_1d_???.????????.xyz | head -n 1) 
bestdat=$(ls -1 tmp_/"$step"_1d_???.????????.dat | head -n 1) 
cp $bestxyz tmp_/"$step"_1d_near.xyz
cp $bestdat tmp_/"$step"_1d_near.dat
