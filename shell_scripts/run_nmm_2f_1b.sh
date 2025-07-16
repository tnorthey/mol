#!/bin/bash

#list=(18 19 20 19 20 21 20 21 22 21 22 23 22 23 24 23 24 25 24 25 26 25 26 27)
list=(27 28 28 29 29 30 30 31 31 32 32 33 33 34 34 35 35 36 36 37 37 38 38)
length=${#list[@]}

for (( i=1; i<$length; i++ ))
do
    echo ${list[i-1]} ${list[i]}
    ./run_nmm_top_4.sh ${list[i-1]} ${list[i]}
done
