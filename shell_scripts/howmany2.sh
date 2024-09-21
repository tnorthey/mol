#!/bin/bash

target_dir=$1

for step in {18..38}
#for step in {0..9}
#for step in {0..12}
do
        echo "step $step has N xyz files:"
        ls "$target_dir"/"$step"_1d_???.*xyz | wc -l
done
