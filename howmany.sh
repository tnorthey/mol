#!/bin/bash

target_dir=$1

for step in {05..75..5}
do
        echo "step $step has N xyz files:"
        ls "$target_dir"/"$step"_???.*xyz | wc -l
done
