#!/bin/bash

previous_step_number=$1
next_step_number=$2
results_dir="tmp_"

# takes random 4 from top 20
top4_xyz_list=$(ls -1 "$results_dir"/"$previous_step_number"_???.*.xyz | head -n 20 | shuf | head -n 4)

for xyz_start_file in $top4_xyz_list
do
    python run.py $next_step_number $xyz_start_file data_/nmm/target_"$next_step_number".dat &
done

sleep 0.1 # For sequential output
echo "Waiting for processes to finish" 
wait $(jobs -p)
echo "All processes finished"
