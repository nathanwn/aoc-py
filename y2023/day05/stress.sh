#!/bin/bash

for((i = 1; ; ++i)); do
    printf "\n"
    printf "============\n"
    echo "Random Test $i"
    printf "============\n"
    python3 gen.py $i > inp.txt
    python3 main.py 2 inp.txt || break
    # ./slow < inp.txt > ans.txt
    # diff -w out.txt ans.txt || break
done
