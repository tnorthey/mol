#!/bin/bash

for i in results_noise*/
do
	echo "tarring $i..."
	tar cf ${i%/*}.tar $i
done
