#!/bin/bash

#starting_xyz_file="tmp_/$(($step-10))_1d_near.xyz"
run_id='1d'
starting_xyz_file=$1
ringclosed=$2  # "closed" or "open"
target_xyz_files="xyz/target_traj094/target_20.xyz,xyz/target_traj094/target_35.xyz,xyz/target_traj094/target_40.xyz,xyz/target_traj094/target_45.xyz,xyz/target_traj094/target_50.xyz,xyz/target_traj094/target_55.xyz,xyz/target_traj094/target_60.xyz,xyz/target_traj094/target_65.xyz,xyz/target_traj094/target_70.xyz,xyz/target_traj094/target_75.xyz"
#python3 -m cProfile run_1D_chd.py $run_id $starting_xyz_file $target_xyz_file $ringclosed
python3 run_1D_chd.py $run_id $starting_xyz_file $target_xyz_files $ringclosed

bestxyz=$(ls -1 tmp_/"$step"_1d_???.????????.xyz | head -n 1) 
bestdat=$(ls -1 tmp_/"$step"_1d_???.????????.dat | head -n 1) 
cp $bestxyz tmp_/"$step"_1d_near.xyz
cp $bestdat tmp_/"$step"_1d_near.dat
