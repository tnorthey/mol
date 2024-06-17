#!/bin/bash

for i in ../results_/results_noise16.0_qmax*_nrestarts5_traj09*/
do
    base_name=$(basename ${i})
    echo $base_name
    ./analysis_script_tdense.sh $i $base_name
done
