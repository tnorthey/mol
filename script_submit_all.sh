#!/bin/bash

constraints="weak"  # "strong" or "weak" constraints, defined in the run.py file
ending="_single_target_20"  # descriptive string that gets appended to files

#for traj in 090 094 099
for traj in 094
do
    for qmax in 4 8
    do
        #for noise in 0.0 0.1 1.0 2.0 4.0 8.0 16.0
        for noise in 0.0 0.1
        do
            tmpfile="tmp_"$traj"_"$qmax"_"$noise"_"$constraints"_"$ending""
            sed "s/_NOISE_/$noise/" SUBMISSION_SCRIPT_TEMPLATE.sh > $tmpfile
            sed -i "s/_QMAX_/$qmax/" $tmpfile
            sed -i "s/_TRAJ_/$traj/" $tmpfile
            sed -i "s/_CONSTRAINTS_/$constraints/" $tmpfile
            sed -i "s/_ENDING_/$ending/" $tmpfile
            chmod +x $tmpfile
            ./$tmpfile
        done
    done
done
