#!/bin/bash

for j in {18..54}
do
    echo $j
    for i in "$j"_1d_???.*xyz ; do head -n 2 $i | tail -n 1 | awk '{print $5 " " $6}'; done > "$j"_torsion.dat
done

grep_plus_minus() {
    grep "^-" "$1"_torsion_grep.dat > "$1"_torsion_grep_minus.dat
    grep -v "^-" "$1"_torsion_grep.dat > "$1"_torsion_grep_plus.dat
}

grep "324.9[89]" 18_torsion.dat > 18_torsion_grep.dat
grep "324.9" 19_torsion.dat > 19_torsion_grep.dat
grep "324.89" 19_torsion.dat >> 19_torsion_grep.dat
grep "324.9" 20_torsion.dat > 20_torsion_grep.dat
grep "324.8[6789]" 20_torsion.dat >> 20_torsion_grep.dat
grep "324.[89]" 21_torsion.dat > 21_torsion_grep.dat
grep "324.7[89]" 21_torsion.dat >> 21_torsion_grep.dat
grep "324.[89]" 22_torsion.dat > 22_torsion_grep.dat
grep "324.7[4-9]" 22_torsion.dat >> 22_torsion_grep.dat
grep "324.[6-9]" 23_torsion.dat > 23_torsion_grep.dat
grep "324.5[89]" 23_torsion.dat >> 23_torsion_grep.dat
grep "324.[4-9]" 24_torsion.dat > 24_torsion_grep.dat
grep "324.[3-9]" 25_torsion.dat > 25_torsion_grep.dat
grep "324.[3-9]" 26_torsion.dat > 26_torsion_grep.dat
grep "324.2[789]" 26_torsion.dat >> 26_torsion_grep.dat
grep "324.[3-9]" 27_torsion.dat > 27_torsion_grep.dat
grep "324.[2-9]" 28_torsion.dat > 28_torsion_grep.dat
grep "324.[2-9]" 29_torsion.dat > 29_torsion_grep.dat
grep "324.[1-9]" 30_torsion.dat > 30_torsion_grep.dat
grep "324.[1-9]" 31_torsion.dat > 31_torsion_grep.dat
grep "324.[1-9]" 32_torsion.dat > 32_torsion_grep.dat
grep "324.[2-9]" 33_torsion.dat > 33_torsion_grep.dat
grep "324.1[5-9]" 33_torsion.dat >> 33_torsion_grep.dat
grep "324.[2-9]" 34_torsion.dat > 34_torsion_grep.dat
grep "324.1[6789]" 34_torsion.dat >> 34_torsion_grep.dat
grep "324.[2-9]" 35_torsion.dat > 35_torsion_grep.dat
grep "324.1[789]" 35_torsion.dat >> 35_torsion_grep.dat

grep "324.[2-9]" 36_torsion.dat > 36_torsion_grep.dat
grep "324.1[5-9]" 36_torsion.dat >> 36_torsion_grep.dat

grep "324.[2-9]" 37_torsion.dat > 37_torsion_grep.dat
grep "324.1[5-9]" 37_torsion.dat >> 37_torsion_grep.dat

grep "324.[2-9]" 37_torsion.dat > 37_torsion_grep.dat
grep "324.[2-9]" 38_torsion.dat > 38_torsion_grep.dat
grep "324.[2-9]" 39_torsion.dat > 39_torsion_grep.dat
grep "324.[2-9]" 40_torsion.dat > 40_torsion_grep.dat
grep "324.[2-9]" 41_torsion.dat > 41_torsion_grep.dat
grep "324.[2-9]" 42_torsion.dat > 42_torsion_grep.dat
grep "324.[2-9]" 43_torsion.dat > 43_torsion_grep.dat
grep "324.[2-9]" 44_torsion.dat > 44_torsion_grep.dat
grep "324.[2-9]" 45_torsion.dat > 45_torsion_grep.dat
grep "324.[2-9]" 46_torsion.dat > 46_torsion_grep.dat
grep "324.[2-9]" 47_torsion.dat > 47_torsion_grep.dat
grep "324.[2-9]" 48_torsion.dat > 48_torsion_grep.dat
grep "324.[2-9]" 49_torsion.dat > 49_torsion_grep.dat
grep "324.[2-9]" 50_torsion.dat > 50_torsion_grep.dat
grep "324.[2-9]" 51_torsion.dat > 51_torsion_grep.dat
grep "324.[2-9]" 52_torsion.dat > 52_torsion_grep.dat
grep "324.[2-9]" 53_torsion.dat > 53_torsion_grep.dat
grep "324.[2-9]" 54_torsion.dat > 54_torsion_grep.dat

for i in {18..54}
do
    grep_plus_minus $i
    total=$(wc -l "$i"_torsion.dat)
    grep_total=$(wc -l "$i"_torsion_grep.dat)
    echo "$grep_total / $total"
done

for sign in plus minus
do
    for i in {18..54}
    do
        torsion_file="$i"_torsion_grep_"$sign".dat
        
        mean_1=$(awk '{ sum += $1; count++ } END { if (count > 0) print sum / count; }' $torsion_file)
        
        
        sd_1=$(awk -v mean=$mean_1 '
        {
            sum_sq_diff += ($1 - mean)^2
            count++
        }
        END {
            variance = sum_sq_diff / count
            printf "%10.8f\n", sqrt(variance)
        }
        ' $torsion_file)
        
        echo "$sign, $i: $mean_1 +/- $sd_1"
        done
done

