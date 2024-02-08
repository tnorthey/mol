#!/bin/bash

for i in {000..999}; do sbatch ccv_start_initial.sh ; done
sleep 10m
./submit_all_XX_YY.sh 10 20
sleep 15m
./submit_all_XX_YY.sh 20 30
sleep 15m
./submit_all_XX_YY.sh 30 35
sleep 15m
./submit_all_XX_YY.sh 35 40
sleep 15m
./submit_all_XX_YY.sh 40 50
sleep 15m
./submit_all_XX_YY.sh 50 60
