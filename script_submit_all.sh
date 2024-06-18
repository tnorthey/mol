#!/bin/bash

for traj in 090 094 099
do
    for qmax in 4 8
    do
        for noise in 0.0 0.1 1.0 2.0 4.0 8.0 16.0
        do
            sed "s/_NOISE_/$noise/" SUBMISSION_SCRIPT_TEMPLATE.sh > tmp
            sed -i "s/_QMAX_/$qmax/" tmp
            sed -i "s/_TRAJ_/$traj/" tmp
            chmod +x tmp
	    head -n 13 tmp | tail -n 7
            ./tmp
        done
    done
done
