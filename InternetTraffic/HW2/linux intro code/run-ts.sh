#!/bin/bash

echo Start $(date +%s) $(date)
ping -DnO -c 3 ${1:-www.aalto.fi}
