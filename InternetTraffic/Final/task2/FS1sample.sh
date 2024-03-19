#!/bin/bash

dir="/var/tmp/urrutia1/flow-continue/"
output_file_ipv4="FS1_sample_ipv4.txt"
output_file_ipv6="FS1_sample_ipv6.txt"

> "$output_file_ipv4"
> "$output_file_ipv6"

for file in "$dir"*
do
    # Print the filename (helps in tracking progress)
    echo "$file"
    # Separate lines corresponding to IPv4 and IPv6
    grep -v '^#' "$file" | grep '\.' | shuf -n 50 >> "$output_file_ipv4"
    grep -v '^#' "$file" | grep ':' | shuf -n 50 >> "$output_file_ipv6"
done
done