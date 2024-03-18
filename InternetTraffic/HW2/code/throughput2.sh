iperf3 -c ok1.iperf.comnet-student.eu -p $((RANDOM % 11 + 5200)) -J > /home/aurruti/Aalto/InternetTraffic/HW2/throughput-log/ok1N$(date +%s).json
iperf3 -c ok1.iperf.comnet-student.eu -p $((RANDOM % 11 + 5200)) -R -J > /home/aurruti/Aalto/InternetTraffic/HW2/throughput-log/ok1R$(date +%s).json
iperf3 -c sgp1.iperf.comnet-student.eu -p $((RANDOM % 11 + 5200)) -J > /home/aurruti/Aalto/InternetTraffic/HW2/throughput-log/sgp1N$(date +%s).json
iperf3 -c sgp1.iperf.comnet-student.eu -p $((RANDOM % 11 + 5200)) -R -J > /home/aurruti/Aalto/InternetTraffic/HW2/throughput-log/sgp1R$(date +%s).json
