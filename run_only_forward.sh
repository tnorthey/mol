#!/bin/bash

results_dir=$1  # 1st command line arg

list=(10 20 32 37 40 45 50 55 60 65 70 75)
length=${#list[@]}

#./run_initial_step.sh;
#for (( i=1; i<$length; i++ ))

for (( i=11; i<$length; i++ ))
do
    echo ${list[i-1]} ${list[i]}
    ./run_top_8.sh $results_dir ${list[i-1]} ${list[i]}
done
