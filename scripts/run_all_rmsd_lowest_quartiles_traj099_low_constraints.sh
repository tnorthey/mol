#!/bin/bash

traj=099

for qmax in 4 8
do

    fname=rmsd_lowest_quartile_qmax"$qmax"_traj"$traj"_low_constraints.dat
    rm $fname || true
    
    for noise in 0.0 0.1 1.0 2.0 4.0
    do
        ./rmsd_lowest_quartile.sh $noise $qmax $traj 1
    done >> $fname

done
