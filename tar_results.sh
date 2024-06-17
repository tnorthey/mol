#!/bin/bash

for i in results_noise16.0*/
do
	echo "tarring $i..."
	tar cf ${i%/*}.tar $i
done
