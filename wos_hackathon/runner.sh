#!/bin/bash


for f in $(echo *csv)
do
    echo "============================================================="
    echo "Processing $f"
    ./extract.py -s $f -t ${f%.csv}
    sed 's/\"\\\\N\"/\"NULL\"/g' -i ${f%.csv}.sql 
done



