#!/bin/bash

awk '{print $3 < '$2'}' $1 | awk '{s+=$1} END {printf "%.0f\n", s}'
