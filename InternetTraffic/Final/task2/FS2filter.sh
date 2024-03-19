#!/bin/bash

output_file=~/FS2-continue.t2

> $output_file

for file in $(find /var/tmp/urrutia1/flow-continue -type f -name "*.t2"); do
    # Use gawk to filter and append to the output file
    gawk '$1~/^163\.35\.116\./||$2~/^163\.35\.116\./' $file >> $output_file
done