#!/bin/bash

echo "Testing "
time ./driver.py -s /mnt/data/WR_1985_20160322043442_DSSHPSH_0001.xml
df -h
time ./driver.py -s /mnt/data/WR_2015_20160212115311_DSSHPSH_0001.xml
