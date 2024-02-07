#!/bin/bash

# for i in $(cat XX_start_list_YY.txt) ; do ./go_1D_chd_qmax8_ZZ_.sh $i; done

step=$1

./create_start_list.sh $step

for i in {0..39}
do
  fname=ccv_start_"$step"_"$i".sh
  cp ccv_start_template.sh $fname
  sed -i "s/XX/$step/" $fname
  sed -i "s/YY/$i/"    $fname
  for j in {0..4}
  do
    sbatch $fname
  done
  #rm $fname
done

