#!/bin/bash

traj_number=$1  # 090, 094, etc.

# Initialise a small pools at steps 2 & 3
./run_top_8.sh 10 20 $traj_number
./run_top_8.sh 10 20 $traj_number
./run_top_8.sh 20 32 $traj_number

