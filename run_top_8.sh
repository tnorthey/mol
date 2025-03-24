#!/bin/bash

results_dir=$1
previous_step_number=$2
next_step_number=$3
traj_number=094

top8_xyz_list=$(ls -1 "$results_dir"/"$previous_step_number"_???.*.xyz | head -n 8)

for xyz_start_file in $top8_xyz_list
do
    python run.py $next_step_number $xyz_start_file xyz/target_traj"$traj_number"/target_"$next_step_number".xyz &
done

sleep 0.1 # For sequential output
echo "Waiting for processes to finish" 
wait $(jobs -p)
echo "All processes finished"