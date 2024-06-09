#!/bin/bash

for i in ../results_/results_noise*_qmax*_nrestarts5_traj094
do
    base_name=$(basename ${i})
    ./analysis_script_tdense.sh $i $base_name
done
