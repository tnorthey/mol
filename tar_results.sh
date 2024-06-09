#!/bin/bash

for i in results_*/
do
	echo "tarring $i..."
	tar cf ${i%/*}.tar $i
done
