#!/bin/bash

target_number=$1 

# run multiple times to make a larger initial pool
for j in {0..4}
do
    for i in {0..3}
    do
        python run.py $target_number xyz/nmm_start.xyz data_/nmm/target_"$target_number".dat &
    done
    
    sleep 0.1 # For sequential output
    echo "Waiting for processes to finish" 
    wait $(jobs -p)
    echo "All processes finished"
done
