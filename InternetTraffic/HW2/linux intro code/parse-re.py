#!/usr/bin/env python3

import sys
import re

if (len(sys.argv)<2):
  print("Give input file name")
  sys.exit()

ping=re.compile('\[(\d+\.\d+)\] .* icmp_seq=(\d+) ttl=\d+ time=(\d+\.?\d*) ms')
pong=re.compile('\[(\d+\.\d+)\] no answer yet for icmp_seq=(\d+)')

for line in open(sys.argv[1]):
  if 'no answer yet' in line:
    m=pong.match(line)
    if m is None:
      # failed for some reason
      continue
    # use -1 as time for lost packet
    print('\t'.join([m[1], m[2], str(-1)]))
  elif 'time=' in line:
    m=ping.match(line)
    if m is None:
      continue
    # print timestamp, sequence and RTT delay
    print('\t'.join([m[1], m[2], m[3]]))
  else:
    print('> ' + line, end='')
