#!/bin/bash

dir="for_paper_nmm_experiment_fitting/tmp_0p1_allbondsangles"

for j in {20..48}
do
    for i in "$dir"/"$j"_0*.xyz
    do

    echo $i
    value=$(python3 thomas_python_dihedral_fix.py "$i")
    #sed -i "2s/\$/ $value/" $i

    awk -v v="$value" '
      NR == 2 {
        if (NF < 9) {
          for (i = NF + 1; i < 9; i++) $i = ""
        }
        $9 = v
      }
      { print }
    ' "$i" > tmp && mv tmp "$i"


    done
done

