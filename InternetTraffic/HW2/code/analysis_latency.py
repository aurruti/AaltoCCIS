# File analysis_latency.py
# Aitor Urruticoechea Puig - 2023

import pandas as pd
from datetime import datetime
import os
import numpy as np

## PATHS

own_path = os.path.dirname(os.path.abspath(__file__))
nameservers_path = own_path + "/24hlog/latency-log/nameservers.log"
research_path = own_path + "/24hlog/latency-log/research.log"
iperf_path = own_path + "/24hlog/latency-log/iperf.log"

## NAMESERVERS
# Note that due to the structure of the .log file, it is easier to do this than to load it directly into a DataFrame
timestamps = []
nameserver_list = []
packets_transmitted = []
packets_received = []
packet_loss = []
timems = []
rtt_min = []
rtt_avg = []
rtt_max = []
rtt_mdev = []
time_starttransfer = []
time_pretransfer = []
time_connect = []
total_latency = []

with open(nameservers_path, 'r') as file:
    lines = file.readlines()
    now_timestamp = None
    line_index = 0
    for line in lines:
        line = line.strip()
        try:
            now_timestamp = (datetime.strptime(line, '%a %b %d %H:%M:%S %Z %Y')).strftime('%Y-%m-%d %H:%M:%S')
        except:
            pass
        if line.startswith('f.') or line.startswith('g.') or line.startswith('e.'):
            now_nameserver = line
            timestamps.append(now_timestamp)
            nameserver_list.append(now_nameserver)
            # If connection is not possible, the next two lines will not include ping data
            try:
                if not("packets" in lines[line_index+1]):
                    packets_transmitted.append(5)
                    packets_received.append(0)
                    packet_loss.append(100)
                    timems.append(float('inf'))
                if not("rtt" in lines[line_index+2]):
                    rtt_min.append(float('inf'))
                    rtt_avg.append(float('inf'))
                    rtt_max.append(float('inf'))
                    rtt_mdev.append(float('inf'))
            except:
                packets_transmitted.append(5)
                packets_received.append(0)
                packet_loss.append(100)
                timems.append(float('inf'))
                rtt_min.append(float('inf'))
                rtt_avg.append(float('inf'))
                rtt_max.append(float('inf'))
                rtt_mdev.append(float('inf'))
        elif "packets" in line:
            ping = line.split (',')
            packets_transmitted.append(int(ping[0].strip(' packets transmitted')))
            packets_received.append(int(ping[1].strip(' packets received')))
            packet_loss.append(float(ping[2].strip('% packet loss')))
            timems.append(int(ping[3].strip('time ms')))      
        elif "rtt" in line:
            rtt = line.strip('rtt min/avg/max/mdev = ms').split('/')
            rtt_min.append(float(rtt[0]))
            rtt_avg.append(float(rtt[1]))
            rtt_max.append(float(rtt[2]))
            rtt_mdev.append(float(rtt[3]))
        elif "CURL" in line:
            dig = line.strip('CURL: ').split(' ')
            time_starttransfer.append(float(dig[0]))
            time_pretransfer.append(float(dig[1]))
            time_connect.append(float(dig[2]))
            total_latency.append(float(dig[0])+float(dig[1]))
        line_index += 1

nameservers_pingdata = pd.DataFrame({
    'Timestamp': timestamps,
    'Nameserver': nameserver_list,
    'Packets Transmitted': packets_transmitted,
    'Packets Received': packets_received,
    'Packet Loss %': packet_loss,
    'Time (ms)' : timems,
    'RTT Min (ms)': rtt_min,
    'RTT Avg (ms)': rtt_avg,
    'RTT Max (ms)': rtt_max,
    'RTT Mdev (ms)': rtt_mdev
})
nameservers_digdata = pd.DataFrame({
    'Timestamp' : timestamps,
    'Nameserver': nameserver_list,
    'Time Start Transfer' : time_starttransfer,
    'Time Pre Transfer' : time_pretransfer,
    'Time Connect' : time_connect,
    'Total Latency' : total_latency
})

## RESEARCH Servers
timestamps = []
nameserver_list = []
packets_transmitted = []
packets_received = []
packet_loss = []
timems = []
rtt_min = []
rtt_avg = []
rtt_max = []
rtt_mdev = []
with open(research_path, 'r') as file:
    lines = file.readlines()
    now_timestamp = None
    line_index = 0
    for line in lines:
        line = line.strip()
        try:
            now_timestamp = (datetime.strptime(line, '%a %b %d %H:%M:%S %Z %Y')).strftime('%Y-%m-%d %H:%M:%S')
        except:
            pass    
        if line.startswith('bcn') or line.startswith('mnl') or line.startswith('hnl'):
            now_nameserver = line
            timestamps.append(now_timestamp)
            nameserver_list.append(now_nameserver)
            # If connection is not possible, the next two lines will not include ping data
            try:
                if not("packets" in lines[line_index+1]):
                    packets_transmitted.append(5)
                    packets_received.append(0)
                    packet_loss.append(100)
                    timems.append(float('inf'))
                if not("rtt" in lines[line_index+2]):
                    rtt_min.append(float('inf'))
                    rtt_avg.append(float('inf'))
                    rtt_max.append(float('inf'))
                    rtt_mdev.append(float('inf'))
            except:
                packets_transmitted.append(5)
                packets_received.append(0)
                packet_loss.append(100)
                timems.append(float('inf'))
                rtt_min.append(float('inf'))
                rtt_avg.append(float('inf'))
                rtt_max.append(float('inf'))
                rtt_mdev.append(float('inf'))
        elif "packets" in line:
            ping = line.split (',')
            packets_transmitted.append(int(ping[0].strip(' packets transmitted')))
            packets_received.append(int(ping[1].strip(' packets received')))
            packet_loss.append(float(ping[2].strip('% packet loss')))
            timems.append(int(ping[3].strip('time ms')))      
        elif "rtt" in line:
            rtt = line.strip('rtt min/avg/max/mdev = ms').split('/')
            rtt_min.append(float(rtt[0]))
            rtt_avg.append(float(rtt[1]))
            rtt_max.append(float(rtt[2]))
            rtt_mdev.append(float(rtt[3]))
        line_index += 1

research_pingdata = pd.DataFrame({
    'Timestamp': timestamps,
    'Research server': nameserver_list,
    'Packets Transmitted': packets_transmitted,
    'Packets Received': packets_received,
    'Packet Loss %': packet_loss,
    'Time (ms)' : timems,
    'RTT Min (ms)': rtt_min,
    'RTT Avg (ms)': rtt_avg,
    'RTT Max (ms)': rtt_max,
    'RTT Mdev (ms)': rtt_mdev
})

## IPERF Servers
timestamps = []
nameserver_list = []
packets_transmitted = []
packets_received = []
packet_loss = []
timems = []
rtt_min = []
rtt_avg = []
rtt_max = []
rtt_mdev = []
curl_namelookup = []
curl_timeconnect = []
curl_timestart = []
curl_timetotal = []
total_latency = []

with open(iperf_path, 'r') as file:
    lines = file.readlines()
    now_timestamp = None
    line_index = 0
    for line in lines:
        line = line.strip()
        try:
            now_timestamp = (datetime.strptime(line, '%a %b %d %H:%M:%S %Z %Y')).strftime('%Y-%m-%d %H:%M:%S')
        except:
            pass    
        if line.startswith('ok1') or line.startswith('sgp1'):
            now_nameserver = line
            timestamps.append(now_timestamp)
            nameserver_list.append(now_nameserver)
            # If connection is not possible, the next two lines will not include ping data
            try:
                if not("packets" in lines[line_index+1]):
                    packets_transmitted.append(5)
                    packets_received.append(0)
                    packet_loss.append(100)
                    timems.append(float('inf'))
                if not("rtt" in lines[line_index+2]):
                    rtt_min.append(float('inf'))
                    rtt_avg.append(float('inf'))
                    rtt_max.append(float('inf'))
                    rtt_mdev.append(float('inf'))
                    curl_namelookup.append(float('inf'))
                    curl_timeconnect.append(float('inf'))
                    curl_timestart.append(float('inf'))
                    curl_timetotal.append(float('inf'))
                    total_latency.append(float('inf'))
            except:
                packets_transmitted.append(5)
                packets_received.append(0)
                packet_loss.append(100)
                timems.append(float('inf'))
                rtt_min.append(float('inf'))
                rtt_avg.append(float('inf'))
                rtt_max.append(float('inf'))
                rtt_mdev.append(float('inf'))
                curl_namelookup.append(float('inf'))
                curl_timeconnect.append(float('inf'))
                curl_timestart.append(float('inf'))
                curl_timetotal.append(float('inf'))
                total_latency.append(float('inf'))
        elif "packets" in line:
            ping = line.split (',')
            packets_transmitted.append(int(ping[0].strip(' packets transmitted')))
            packets_received.append(int(ping[1].strip(' packets received')))
            packet_loss.append(float(ping[2].strip('% packet loss')))
            timems.append(int(ping[3].strip('time ms')))      
        elif "rtt" in line:
            rtt = line.strip('rtt min/avg/max/mdev = ms').split('/')
            rtt_min.append(float(rtt[0]))
            rtt_avg.append(float(rtt[1]))
            rtt_max.append(float(rtt[2]))
            rtt_mdev.append(float(rtt[3]))
            curl = lines[line_index+1].strip().split(',')
            curl_namelookup.append(float(curl[0]))
            curl_timeconnect.append(float(curl[1]))
            curl_timestart.append(float(curl[2]))
            curl_timetotal.append(float(curl[3]))
            total_latency.append(float(curl[1])-float(curl[0]))
        line_index += 1

iperf_pingdata = pd.DataFrame({
    'Timestamp': timestamps,
    'Iperf server': nameserver_list,
    'Packets Transmitted': packets_transmitted,
    'Packets Received': packets_received,
    'Packet Loss %': packet_loss,
    'Time (ms)' : timems,
    'RTT Min (ms)': rtt_min,
    'RTT Avg (ms)': rtt_avg,
    'RTT Max (ms)': rtt_max,
    'RTT Mdev (ms)': rtt_mdev
})

iperf_curldata = pd.DataFrame({
    'Timestamp': timestamps,
    'Iperf server': nameserver_list,
    'Namelookup (ms)' : curl_namelookup,
    'Connect Time(ms)' : curl_timeconnect,
    'Start Time (ms)' : curl_timestart,
    'Total Time (ms)' : curl_timetotal,
    'Total Latency' : total_latency
})

## Data interpretation
# Nameservers

medianping_nameservers = nameservers_pingdata.groupby('Nameserver')['RTT Avg (ms)'].median()
meanping_nameservers = nameservers_pingdata.replace(float('inf'),np.nan).groupby('Nameserver')['RTT Avg (ms)'].mean()
lossping_nameservers = 100*(nameservers_pingdata.groupby('Nameserver')['Packets Transmitted'].sum() - nameservers_pingdata.groupby('Nameserver')['Packets Received'].sum()) / nameservers_pingdata.groupby('Nameserver')['Packets Received'].sum()
delayspreadping_nameservers = nameservers_pingdata.groupby('Nameserver')['RTT Avg (ms)'].quantile(0.75) - nameservers_pingdata.groupby('Nameserver')['RTT Avg (ms)'].quantile(0.25)

mediandig_nameservers = nameservers_digdata.replace(float(0), float('inf')).groupby('Nameserver')['Total Latency'].median()
meandig_nameservers = nameservers_digdata.replace(float(0),np.nan).groupby('Nameserver')['Total Latency'].mean()
dig_nameservers_countloss = nameservers_digdata[nameservers_digdata['Time Start Transfer'] == float(0)].groupby('Nameserver').size()
dig_nameservers_countnoloss = nameservers_digdata[nameservers_digdata['Time Start Transfer'] != float(0)].groupby('Nameserver').size()
lossdig_nameservers = (100*dig_nameservers_countloss / (dig_nameservers_countloss+dig_nameservers_countnoloss)).replace(np.nan, 0)
delayspreaddig_nameservers = nameservers_digdata.groupby('Nameserver')['Total Latency'].quantile(0.75) - nameservers_digdata.groupby('Nameserver')['Total Latency'].quantile(0.25)


# Research servers
medianping_research = research_pingdata.groupby('Research server')['RTT Avg (ms)'].median()
meanping_research = research_pingdata.replace(float('inf'),np.nan).groupby('Research server')['RTT Avg (ms)'].mean()
lossping_research = 100*(research_pingdata.groupby('Research server')['Packets Transmitted'].sum() - research_pingdata.groupby('Research server')['Packets Received'].sum()) / research_pingdata.groupby('Research server')['Packets Received'].sum()
delayspreadping_research = research_pingdata.groupby('Research server')['RTT Avg (ms)'].quantile(0.75) - research_pingdata.groupby('Research server')['RTT Avg (ms)'].quantile(0.25)

# Iperf servers
medianping_iperf = iperf_pingdata.groupby('Iperf server')['RTT Avg (ms)'].median()
meanping_iperf = iperf_pingdata.replace(float('inf'),np.nan).groupby('Iperf server')['RTT Avg (ms)'].mean()
lossping_iperf = 100*(iperf_pingdata.groupby('Iperf server')['Packets Transmitted'].sum() - iperf_pingdata.groupby('Iperf server')['Packets Received'].sum()) / iperf_pingdata.groupby('Iperf server')['Packets Received'].sum()
delayspreadping_iperf = iperf_pingdata.groupby('Iperf server')['RTT Avg (ms)'].quantile(0.75) - iperf_pingdata.groupby('Iperf server')['RTT Avg (ms)'].quantile(0.25)

mediancurl_iperf = iperf_curldata.groupby('Iperf server')['Total Latency'].median()
meancurl_iperf = iperf_curldata.replace(float('inf'),np.nan).groupby('Iperf server')['Total Latency'].mean()
curl_iperf_countloss = iperf_curldata[iperf_curldata['Total Latency'] == float('inf')].groupby('Iperf server').size()
curl_iperf_countnoloss = iperf_curldata[iperf_curldata['Total Latency'] != float('inf')].groupby('Iperf server').size()
losscurl_iperf = (100*curl_iperf_countloss / (curl_iperf_countloss+curl_iperf_countnoloss) ).replace(np.nan, 0)
delayspreadcurl_iperf = iperf_curldata.groupby('Iperf server')['Total Latency'].quantile(0.75) - iperf_curldata.groupby('Iperf server')['Total Latency'].quantile(0.25)



