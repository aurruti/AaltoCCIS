export LANG=C

echo -e $(date +%s)", \c" >> /home/aurruti/Aalto/InternetTraffic/HW2/throughput-log/method1.csv
curl -w "%{http_code}, %{speed_download}, " -o /dev/null -s http://ok1.iperf.comnet-student.eu/10M.bin >> /home/aurruti/Aalto/InternetTraffic/HW2/throughput-log/method1.csv
curl -w "%{http_code}, %{speed_download}\\n" -o /dev/null -s http://sgp1.iperf.comnet-student.eu/10M.bin >> /home/aurruti/Aalto/InternetTraffic/HW2/throughput-log/method1.csv
