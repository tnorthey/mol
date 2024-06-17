#!/bin/bash

#for noise in 0.0 0.1 1.0 2.0 4.0
for noise in 8.0 16.0
do
   sed "s/_NOISE_/$noise/" SUBMISSION_SCRIPT_TEMPLATE.sh > tmp
   chmod +x tmp
   ./tmp
done
