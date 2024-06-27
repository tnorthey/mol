#!/bin/bash

lt_file="vmd_open_lt_x.sh"
gt_file="vmd_open_gt_x.sh"
echo -n 'vmd -m ' > $lt_file
echo -n 'vmd -m ' > $gt_file

for i in 20_1d_???.*.xyz
do
    rmsd=$(head -n 2 $i | tail -n 1 | awk '{print $2}')
    if awk "BEGIN {exit !($rmsd < 0.21)}"
    then
       echo -n "$i " >> $lt_file
    else
       echo -n "$i " >> $gt_file
    fi
done

echo -n '20_1d_target.xyz' >> $lt_file
echo -n '20_1d_target.xyz' >> $gt_file
chmod +x $lt_file $gt_file
