#!/bin/bash
export LANG=C
fmt="%{time_namelookup}, %{time_connect}, %{time_starttransfer}, %{time_total}\n"
curl -w "$fmt" -o /dev/null -s ${1:-http://www.aalto.fi}
