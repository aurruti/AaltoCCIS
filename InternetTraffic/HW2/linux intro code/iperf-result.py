#!/usr/bin/env python3

import sys
import json

if (len(sys.argv)<2):
  print("Give at least one input file name")
  sys.exit()

for f in sys.argv[1:]:
  with open(f) as jf:
    try:
      ip=json.load(jf)
      print('\t'.join(map(str, [ip['start']['timestamp']['timesecs'],
                                ip['end']['sum_sent']['bits_per_second'],
                                ip['end']['sum_received']['bits_per_second']])))
    except json.decoder.JSONDecodeError:
      pass                    # invalid json file, just ignore
    except KeyError:            # tried to read non existent value
      if 'start' in ip:
        print('\t'.join(map(str, [ip['start']['timestamp']['timesecs'], 0, 0])))
