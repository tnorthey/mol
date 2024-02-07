#!/bin/bash

step=$1
full_list="$step"_full_list.txt
ls -1 tmp_/"$step"_1d_???.*xyz > $full_list

c=0
for i in {5..200..5}
do
head -n $i  $full_list | tail -n 5 > "$step"_start_list_$c.txt
c=$(($c+1))
done
