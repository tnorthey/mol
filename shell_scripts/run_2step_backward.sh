#!/bin/bash

traj_number=$1  # 090 etc.

list=(75 65 55 45 37)
length=${#list[@]}

#./run_initial_step.sh;
for (( i=1; i<$length; i++ ))
do
    echo ${list[i-1]} ${list[i]}
    ./run_top_8.sh ${list[i-1]} ${list[i]} $traj_number
done

list2=(70 60 50 40 32)
length=${#list2[@]}

for (( i=1; i<$length; i++ ))
do
    echo ${list2[i-1]} ${list2[i]}
    ./run_top_8.sh ${list2[i-1]} ${list2[i]} $traj_number
done
