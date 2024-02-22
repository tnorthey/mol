#!/bin/bash

#10 20 32 35 37 40 44 50 55 60 65 70 75

#for i in {000..999}; do sbatch ccv_start_initial.sh ; done
#sleep 15m
#./submit_all_XX_YY.sh 10 20
#sleep 15m
#./submit_all_XX_YY.sh 20 32
#sleep 15m
#./submit_all_XX_YY.sh 32 35
#sleep 9m
#./submit_all_XX_YY.sh 35 37
sleep 7m
./submit_all_XX_YY.sh 37 40
sleep 9m
./submit_all_XX_YY.sh 40 44
sleep 9m
./submit_all_XX_YY.sh 44 50
sleep 9m
./submit_all_XX_YY.sh 50 55
sleep 9m
./submit_all_XX_YY.sh 55 60
sleep 9m
./submit_all_XX_YY.sh 60 65
sleep 9m
./submit_all_XX_YY.sh 65 70
sleep 9m
./submit_all_XX_YY.sh 70 75

