#!/bin/bash

results_dir=$1  # 1st command line arg

list=(10 20 10 20 32 20 10 20 32 37 32 20 32 37 40 37 32 37 40 45 40 37 40 45 50 45 40 45 50 55 50 45 50 55 60 55 50 55 60 65 60 55 60 65 70 65 60 65 70 75 70 65 70 75 70 75 70 65 60 55 50 45 40 37 32 20 10 10 20 20 32 32 37 37 40 40 45 45 50 50 55 55 60 60 65 65 70 70 75 75 70 70 65 65 60 60 55 55 50 50 45 45 40 40 37 37 32 32 20 20 10)
length=${#list[@]}

#./run_initial_step.sh;
#for (( i=1; i<$length; i++ ))

for (( i=15; i<$length; i++ ))
do
    echo ${list[i-1]} ${list[i]}
    ./run_top_8.sh $results_dir ${list[i-1]} ${list[i]}
done