#!/bin/bash

#python3 sine_transform.py 41  0.03   # k = 0.05  is ok
#python3 sine_transform.py 81  0.015   # k = 0.02  looks good
#python3 sine_transform.py 241 0.006  # k = 0.005 looks good

#cd -; python3 sine_transform_noise.py 81 0.015 0; cd -; gnuplot PLOT_SINETRANSFORM_NOISE.gp

cd -; python3 sine_transform_noise.py 81 0.03 1; cd -; gnuplot PLOT_SINETRANSFORM_NOISE.gp
cd -; python3 sine_transform_noise.py 81 0.08 4; cd -; gnuplot PLOT_SINETRANSFORM_NOISE.gp
cd -; python3 sine_transform_noise.py 81 0.12 16; cd -; gnuplot PLOT_SINETRANSFORM_NOISE.gp
