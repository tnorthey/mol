#!/bin/bash

traj_number=$1  # 090 etc.

list=(10 15 20 25 30 32 35 37 40 45 50 55 60 65 70 75)
length=${#list[@]}

#./run_initial_step.sh;
#for (( i=1; i<$length; i++ ))

for (( i=1; i<$length; i++ ))
do
    echo ${list[i-1]} ${list[i]}
    ./run_top_8.sh ${list[i-1]} ${list[i]} $traj_number
done
