#!/bin/bash

traj_number=$1  # 090 etc.

list=(75 70 65 60 55 50 45 40 37 32)
length=${#list[@]}

#./run_initial_step.sh;
for (( i=1; i<$length; i++ ))
do
    echo ${list[i-1]} ${list[i]}
    ./run_top_8.sh ${list[i-1]} ${list[i]} $traj_number
done
