#!/bin/bash

#for i in ../results_/results_noise*_qmax?_nrestarts5_traj09?_low_constraints_c/
for i in ../results_/results_noise*_qmax?_nrestarts5_traj09?_d/
do
    base_name=$(basename ${i})
    echo $base_name
    ./analysis_script_tdense.sh $i $base_name
done
