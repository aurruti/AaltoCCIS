#!/bin/bash
# takes two optional arguments:
# - hostname of iperf server (defaults iperf.funet.fi)
# - seconds to run test for (defaults 10 seconds)

host=${1:-iperf.funet.fi} 
secs=${2:-10}
d=$(date -Isec | tr -d : | sed s/+.*//)
mkdir $d
ping -c $(($secs * 2)) $host > $d/ping-$host.txt &
pingpid=$!
iperf3 -c $host -t $secs -J > $d/iperf3-$host.json
kill -INT $pingpid
wait
