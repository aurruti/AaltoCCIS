date
echo "bcn-es"
ping bcn-es.ark.caida.org -c 5 -O -D | fgrep -e packets -e rtt
echo "mnl-ph"
ping mnl-ph.ark.caida.org -c 5 -O -D | fgrep -e packets -e rtt
echo "hnl-us"
ping hnl-us.ark.caida.org -c 5 -O -D | fgrep -e packets -e rtt