#!/bin/bash

#arr=(20 35 40 45 50 55 60 65 70 75)
#arr=(35 40 45)
#arr=(40 45 50)
#arr=(45 50 55)
#arr=(50 55 60)
arr=(35 40 45 50 55 60 65 70 75)
#arr=(35 45 55 65)
#arr=(40 50 60)

arr_len=${#arr[@]}
END=$(($arr_len-2))

for j in {0..4}
do
for i in $(seq 0 $END)
do
	A=${arr[i]}
	B=${arr[i+1]}
	#echo "$A $B"
	#./backforth_submit.sh $A $B
	echo "$B $A"
	./backforth_submit.sh $B $A
	sleep 30s
done
done
