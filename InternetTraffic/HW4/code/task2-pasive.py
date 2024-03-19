# File task2-pasive.py
# Aitor Urruticoechea 2023
import pyshark
import pandas as pd
from datetime import datetime
import numpy as np
from matplotlib import pyplot as plt

filepath = "task4.pcap"

# From .pcap to DataFrame
packet_data = []
capture = pyshark.FileCapture(filepath)
for packet in capture:
    packet_info = {
        "Timestamp": packet.sniff_time, 
        "Source IP": packet.ip.src if "ip" in packet else None,
        "Destination IP": packet.ip.dst if "ip" in packet else None,
        "Protocol": packet.transport_layer, 
        "Length": packet.length,         
    }
    if 'TCP' in packet:
        packet_info['Transport Protocol'] = 'TCP'
        packet_info['Destination Port'] = int(packet.tcp.dstport)
        packet_info['ICMP Type'] = None
        packet_info['ICMP Id'] = None
    elif 'UDP' in packet:
        packet_info['Transport Protocol'] = 'UDP'
        packet_info['Destination Port'] = int(packet.udp.dstport)
        packet_info['ICMP Type'] = None
        packet_info['ICMP Id'] = None
    elif 'ICMP' in packet:
        packet_info['Transport Protocol'] = 'ICMP'
        packet_info['Destination Port'] = None
        packet_info['ICMP Type'] = int(packet.icmp.type)
        try:
            packet_info['ICMP Id'] = packet.icmp.ident
        except:
            packet_info['ICMP Id'] = None
    else:
        packet_info['Transport Protocol'] = 'Other'
        packet_info['Destination Port'] = None
        packet_info['ICMP Type'] = None
        packet_info['ICMP Id'] = None
    packet_data.append(packet_info)
ws_df = pd.DataFrame(packet_data)
ws_df["Timestamp"] = pd.to_datetime(ws_df["Timestamp"])


# Filtering out iper3 connections:
filter_iperf3 = (
    (ws_df["Source IP"] == "172.26.184.25") &
    (ws_df["Protocol"] == "TCP")
)

iperf3_flows = ws_df[filter_iperf3]

# Calculating throughput
throughput_data = []
##datetime_format = '%Y-%m-%d %H:%M:%S.%f'
##for unique_flow, group in iperf3_flows.groupby(["Source IP", "Destination IP", "Protocol", "Destination Port"]):
##    flow_start_time = group["Timestamp"].min()
##    flow_end_time = group["Timestamp"].max()
##    group['Length'] = group['Length'].apply(lambda x: float(x))
##    data_transferred = group["Length"].sum()
##    try:
##        time_duration = flow_end_time - flow_start_time
##    except:
##        time_duration = datetime.strptime(flow_end_time, datetime_format)-datetime.strptime(flow_start_time, datetime_format)  
##    throughput_bps = (float(data_transferred)*8) / time_duration.total_seconds()
##    throughput_data.append({
##        "Source IP": unique_flow[0],
##        "Destination IP": unique_flow[1],
##        "Protocol": unique_flow[2],
##        "Destination Port": unique_flow[3],
##        "Throughput (bps)": throughput_bps
##    })
##throughput_df = pd.DataFrame(throughput_data)

iperf3_flows = iperf3_flows.sort_values(by=['Timestamp'])
time_interval = pd.Timedelta(minutes=1)
groups = iperf3_flows.groupby(['Source IP', 'Destination IP', pd.Grouper(key='Timestamp', freq=time_interval)])
throughput_data = []
for group_name, group_data in groups:
    group_data['Length'] = group_data['Length'].apply(lambda x: float(x))
    data_exchanged = group_data['Length'].sum()
    time_interval_seconds = float(group_data['Timestamp'].max().second - group_data['Timestamp'].min().second)
    if time_interval_seconds == float(1):
        throughput_bps = data_exchanged * 8
    elif time_interval_seconds == float(0):
        throughput_bps = float('nan')
    else:
        throughput_bps = (data_exchanged * 8) / time_interval_seconds
    throughput_info = {
        'Source IP': group_name[0],
        'Destination IP': group_name[1],
        'Start Timestamp': group_data['Timestamp'].min(),
        'End Timestamp': group_data['Timestamp'].max(),
        'Throughput (bps)': throughput_bps
    }
    
    throughput_data.append(throughput_info)
throughput_df = pd.DataFrame(throughput_data)


# Filtering out ping
filter_icmp = ws_df[ws_df['Transport Protocol'] == 'ICMP']
filter_icmp = filter_icmp.sort_values(by=['Timestamp'])

# Calculating delay
icmp_requests = filter_icmp[filter_icmp['ICMP Type'] == 8]
icmp_responses = filter_icmp[filter_icmp['ICMP Type'] == 0]
icmp_merged = pd.merge(icmp_requests, icmp_responses, on='ICMP Id', how='outer', suffixes=('_request', '_response'))
icmp_merged['Delay'] = icmp_merged['Timestamp_response'] - icmp_merged['Timestamp_request']
icmp_merged['Delay'] = icmp_merged['Delay'].apply(lambda x: abs(x.total_seconds()))
icmp_merged['Packet Loss'] = icmp_merged['Timestamp_response'].isnull()

# Filtering out active measurements
filter_measure = (
    ((ws_df["Source IP"] != "172.26.184.25") &
    (ws_df["Protocol"] == "TCP")) |
    (ws_df['Transport Protocol'] != 'ICMP'))
nomeasure_df = ws_df[filter_measure]
nomeasure_df['Length'] = nomeasure_df['Length'].apply(lambda x: float(x))
print(nomeasure_df['Length'].sum()*8)
#filter_icmp['Length'] = filter_icmp['Length'].apply(lambda x: float(x))
#iperf3_flows['Length'] = iperf3_flows['Length'].apply(lambda x: float(x))


# Plots
fig, ax = plt.subplots(figsize=(12, 6))
ax.scatter(icmp_merged['Timestamp_request'], icmp_merged['Delay'])
ax.set_xlabel('Timestamp')
ax.set_ylabel('Delay (ms)')
ax.set_yscale('log')
ax.grid(True)
plt.show()


fig, ax = plt.subplots(figsize=(12, 6))
throughput_df['Throughput (bps)'] = throughput_df['Throughput (bps)'].apply(lambda x: 0 if str(x) == 'nan' else x)
ax.scatter(throughput_df['Start Timestamp'], throughput_df['Throughput (bps)'])
ax.set_xlabel('Timestamp')
ax.set_ylabel('Throughput (bps)')
ax.set_yscale('log')
ax.grid(True)
plt.show()
