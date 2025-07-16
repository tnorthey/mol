#!/bin/bash

traj_number=$1  # 090 etc.

list=(10 20 32 37 40 45 50 55 60 65 70 75)
length=${#list[@]}

#for j in {0..1}
#do
    for (( i=0; i<$length; i++ ))
    do
        echo ${list[i]} ${list[i]}
        ./run_top_8.sh ${list[i]} ${list[i]} $traj_number
    done
#done
