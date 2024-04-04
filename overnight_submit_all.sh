#!/bin/bash

#10 20 32 35 37 40 44 50 55 60 65 70 75

#for i in {000..999}; do sbatch ccv_start_initial.sh ; done
#for k in 1 2
#do
    #./submit_all_XX_YY.sh 20 35
    #sleep 20m
    #./submit_all_XX_YY.sh 35 40
    #sleep 20m
    #./submit_all_XX_YY.sh 40 45
    #sleep 20m
    #./submit_all_XX_YY.sh 45 50
    #sleep 20m
    #./submit_all_XX_YY.sh 50 55
    #sleep 20m
    #./submit_all_XX_YY.sh 55 60
    #sleep 20m
    #./submit_all_XX_YY.sh 60 65
    #sleep 20m
    #./submit_all_XX_YY.sh 65 70
    #sleep 20m
    #./submit_all_XX_YY.sh 70 75
    ##sleep 20m
    ./submit_all_XX_YY.sh 75 70
    sleep 20m
    ./submit_all_XX_YY.sh 70 65
    sleep 20m
    ./submit_all_XX_YY.sh 65 60
    sleep 20m
    ./submit_all_XX_YY.sh 60 55
    sleep 20m
    ./submit_all_XX_YY.sh 55 50
    sleep 20m
    ./submit_all_XX_YY.sh 50 45
    sleep 20m
    ./submit_all_XX_YY.sh 45 40
    sleep 20m
    ./submit_all_XX_YY.sh 40 35
    sleep 20m
    ./submit_all_XX_YY.sh 35 20
    #sleep 20m
#done
