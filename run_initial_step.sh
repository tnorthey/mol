#!/bin/bash

traj_number=099

# run multiple times to make a larger initial pool
for j in {0..4}
do
    for i in {0..3}
    do
        python run.py 10 xyz/start.xyz xyz/target_traj"$traj_number"/target_10.xyz &
    done
    
    sleep 0.1 # For sequential output
    echo "Waiting for processes to finish" 
    wait $(jobs -p)
    echo "All processes finished"
done
