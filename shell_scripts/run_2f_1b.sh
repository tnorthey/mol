#!/bin/bash

traj_number=$1  # 090, 094, etc.

# Initialise a small pool at the second step
./run_top_8.sh 10 20 $traj_number

list=(10 20 32 20 32 37 32 37 40 37 40 45 40 45 50 45 50 55 50 55 60 55 60 65 60 65 70 65 70 75 70 75)
length=${#list[@]}

#./run_initial_step.sh;
for (( i=1; i<$length; i++ ))
do
    echo ${list[i-1]} ${list[i]}
    ./run_top_8.sh ${list[i-1]} ${list[i]} $traj_number
done
