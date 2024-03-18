export LANG=C
date

echo "ok1"
ping ok1.iperf.comnet-student.eu -c 5 -O -D | fgrep -e packets -e rtt
curl -o /dev/null -w '%{time_namelookup}, %{time_connect}, %{time_starttransfer}, %{time_total}\n' -s ${1:-ok1.iperf.comnet-student.eu/1K:bin:80}

echo "sgp1"
ping sgp1.iperf.comnet-student.eu -c 5 -O -D | fgrep -e packets -e rtt
curl -o /dev/null -w '%{time_namelookup}, %{time_connect}, %{time_starttransfer}, %{time_total}\n' -s ${1:-sgp1.iperf.comnet-student.eu/1K:bin:80}
