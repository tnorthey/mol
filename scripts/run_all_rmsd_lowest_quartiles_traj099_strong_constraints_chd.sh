#!/bin/bash

traj=099
ending="strong_constraints_chd"

for qmax in 4 8
do

    fname=rmsd_lowest_quartile_qmax"$qmax"_traj"$traj"_"$ending".dat
    rm $fname || true
    
    for noise in 0.0 0.1 1.0 2.0 4.0 8.0 16.0
    do
        ./rmsd_lowest_quartile.sh $noise $qmax $traj $ending
    done >> $fname

done
