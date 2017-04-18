#!/bin/bash

for dir in *
do 
	echo -ne "$dir\t" >> test.txt
	head -3 $dir/$dir/*.tbl | tail -1 | cut -f 4 >> test.txt
done
sort -k2nr -k 1 test.txt
