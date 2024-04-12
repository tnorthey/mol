#!/bin/bash

run_id='1d'
starting_xyz_file=$1
ringclosed=$2  # "closed" or "open"
target_xyz_files="xyz/target_traj094/target_20.xyz,xyz/target_traj094/target_35.xyz,xyz/target_traj094/target_40.xyz,xyz/target_traj094/target_45.xyz,xyz/target_traj094/target_50.xyz,xyz/target_traj094/target_55.xyz,xyz/target_traj094/target_60.xyz,xyz/target_traj094/target_65.xyz,xyz/target_traj094/target_70.xyz,xyz/target_traj094/target_75.xyz"
#target_order="0,1,0,1,2,1,0,1,2,3,2,1,0,1,2,3,4,3,2,1,2,3,4,5,4,3,2,3,4,5,6,5,4,3,4,5,6,7,6,5,4,5,6,7,8,7,6,5,6,7,8,9,8,7,6,7,8,9"
#target_order="0,1,0,1,0,1,2,1,2,1,0"   # start from 0
#target_order="1,2,1,2,1,2,3,2,3,2,1"   # start from 1
#target_order="2,3,2,3,2,3,4,3,4,3,2"   # start from 2
#target_order="3,4,3,4,3,4,5,4,5,4,3"   # start from 3
#target_order="4,5,4,5,4,5,6,5,6,5,4"   # start from 4
#target_order="5,6,5,6,5,6,7,6,7,6,5"   # start from 5
#target_order="6,7,6,7,6,7,8,7,8,7,6"   # start from 6
#target_order="7,8,7,8,7,8,9,8,9,8,7"   # start from 7
#target_order="8,9,8,9,8,9"         # start from 8
### here I change to "open", increase gd steps to 40000 from 20000, lower T0 to 0.5 from 1,  and allow all modes in the greedy step
#target_order="9"      # start from x
### here I change to "unrestrained"
target_order="9"      # start from x
python3 run_1D_chd.py $run_id $starting_xyz_file $target_xyz_files $target_order $ringclosed

#bestxyz=$(ls -1 tmp_/"$step"_1d_???.????????.xyz | head -n 1) 
#bestdat=$(ls -1 tmp_/"$step"_1d_???.????????.dat | head -n 1) 
#cp $bestxyz tmp_/"$step"_1d_near.xyz
#cp $bestdat tmp_/"$step"_1d_near.dat
