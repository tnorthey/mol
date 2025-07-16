#!/bin/bash

list=(20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38)
length=${#list[@]}

for (( i=1; i<$length; i++ ))
do
    echo ${list[i-1]} ${list[i]}
    ./run_nmm_top_4.sh ${list[i-1]} ${list[i]}
    ./run_nmm_top_4.sh ${list[i-1]} ${list[i]}
    ./run_nmm_top_4.sh ${list[i-1]} ${list[i]}
done
