#!/bin/bash
join -j1 -o 2.2 1.2\
    <(zcat $1 | awk '$11 == 1{print $3":"$4":"$5":"$6, $9}' | sort -k 1b,1) \
    <(zcat $2 | awk '$11 == 1{print $3":"$4":"$5":"$6, $9}' | sort -k 1b,1)
