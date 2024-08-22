#!/bin/bash

for i in target_traj09?
do
    cp octave_target_traj_surf_script_template.m $i/octave_surf_script.m
    cd $i
    octave octave_surf_script.m
    cd -
    cp $i/surf_plot.png "$i"_surf_plot.png
done
