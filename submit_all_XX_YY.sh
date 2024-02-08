#!/bin/bash

previous_step=$1
step=$2

./create_start_list.sh $previous_step

for i in {0..39}
do
  fname=ccv_start_"$step"_"$i".sh
  cp ccv_start_template.sh $fname
  sed -i "s/XX/$previous_step/" $fname
  sed -i "s/ZZ/$step/" $fname
  sed -i "s/YY/$i/"    $fname
  for j in {0..4}
  do
    echo $fname
    sbatch $fname
  done
  #rm $fname
done

