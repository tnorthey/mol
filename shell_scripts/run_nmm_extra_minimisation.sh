#!/bin/bash

list=(20 21 21 21 21)
length=${#list[@]}

#./run_initial_step.sh;
for (( i=1; i<$length; i++ ))
do
    echo ${list[i-1]} ${list[i]}
    ./run_nmm_top_4.sh ${list[i-1]} ${list[i]}
done
