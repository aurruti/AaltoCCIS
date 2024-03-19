# File AS1analysis.py
# Aitor Urruticoechea 2023
import pandas as pd
from datetime import datetime
import os
from matplotlib import pyplot as plt
import numpy as np

## PATHS
own_path = os.path.dirname(os.path.abspath(__file__))
nameservers_path = own_path + "/latency-log/nameservers.log"
research_path = own_path + "/latency-log/research.log"
iperf_path = own_path + "/latency-log/iperf.log"


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
            line = line.replace('EEST', '')
            now_timestamp = (datetime.strptime(line, '%a %b %d %H:%M:%S %Y')).strftime('%Y-%m-%d %H:%M:%S')
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

AS1_d1 = nameservers_pingdata[nameservers_pingdata['Nameserver'].str.contains("e.ext.nic.fr")]
AS1_d2 = nameservers_pingdata[nameservers_pingdata['Nameserver'].str.contains("g.ext.nic.fr")]
AS1_d3 = nameservers_pingdata[nameservers_pingdata['Nameserver'].str.contains("f.ext.nic.fr")]

nameservers_digdata = pd.DataFrame({
    'Timestamp' : timestamps,
    'Nameserver': nameserver_list,
    'Time Start Transfer' : time_starttransfer,
    'Time Pre Transfer' : time_pretransfer,
    'Time Connect' : time_connect,
    'Total Latency' : total_latency
})

AS1_n1 = nameservers_digdata[nameservers_digdata['Nameserver'].str.contains("e.ext.nic.fr")]
AS1_n2 = nameservers_digdata[nameservers_digdata['Nameserver'].str.contains("g.ext.nic.fr")]
AS1_n3 = nameservers_digdata[nameservers_digdata['Nameserver'].str.contains("f.ext.nic.fr")]

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
            line = line.replace('EEST', '')
            now_timestamp = (datetime.strptime(line, '%a %b %d %H:%M:%S %Y')).strftime('%Y-%m-%d %H:%M:%S')
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

AS1_r1 = research_pingdata[research_pingdata['Research server'].str.contains("bcn")]
AS1_r2 = research_pingdata[research_pingdata['Research server'].str.contains("mnl")]
AS1_r3 = research_pingdata[research_pingdata['Research server'].str.contains("hnl")]

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
            line = line.replace('EEST', '')
            now_timestamp = (datetime.strptime(line, '%a %b %d %H:%M:%S %Y')).strftime('%Y-%m-%d %H:%M:%S')
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

AS1_i1 = iperf_pingdata[iperf_pingdata['Iperf server'].str.contains("ok1")]
AS1_i2 = iperf_pingdata[iperf_pingdata['Iperf server'].str.contains("sgp1")]

## Data interpretation
def create_boxplot_success(dataframe, title):
    try:
        dataframe = dataframe[dataframe['Packet Loss %'] == 0]
    except:
        try:
            dataframe = dataframe[dataframe['Packet Loss %'] == 100]
        except:
            dataframe = dataframe[dataframe['Total Latency'] < float(1000)]
    plt.figure(figsize=(14, 6))
    dataframe.boxplot()
    plt.title('Box Plot - ' + title)
    plt.yscale('log')
    plt.xlabel('Variables')
    plt.ylabel('Values')
    plt.savefig(own_path + '\\boxplots-success\\' + title + '.png')
    plt.show()

def create_boxplot_all(dataframe, title):
    plt.figure(figsize=(14, 6))
    dataframe.boxplot()
    plt.title('Box Plot - ' + title)
    plt.yscale('log')
    plt.xlabel('Variables')
    plt.ylabel('Values')
    plt.savefig(own_path + '\\boxplots-all\\' + title + '.png')
    plt.show()

# create_boxplot_success(AS1_d1, 'AS1 - d1 - e.ext.nic.fr')
# create_boxplot_success(AS1_d2, 'AS1 - d2 - g.ext.nic.fr')
# create_boxplot_success(AS1_d3, 'AS1 - d3 - f.ext.nic.fr')
# create_boxplot_success(AS1_n1, 'AS1 - n1 - e.ext.nic.fr')
# create_boxplot_success(AS1_n2, 'AS1 - n2 - g.ext.nic.fr')
# create_boxplot_success(AS1_n3, 'AS1 - n3 - f.ext.nic.fr')
# create_boxplot_success(AS1_r1, 'AS1 - r1 - bcn')
# create_boxplot_success(AS1_r2, 'AS1 - r2 - mnl')
# create_boxplot_success(AS1_r3, 'AS1 - r3 - hnl')
# create_boxplot_success(AS1_i1, 'AS1 - i1 - ok1')
# create_boxplot_success(AS1_i2, 'AS1 - i2 - sgp1')

# create_boxplot_all(AS1_d1, 'AS1 - d1 - e.ext.nic.fr')
# create_boxplot_all(AS1_d2, 'AS1 - d2 - g.ext.nic.fr')
# create_boxplot_all(AS1_d3, 'AS1 - d3 - f.ext.nic.fr')
# create_boxplot_all(AS1_n1, 'AS1 - n1 - e.ext.nic.fr')
# create_boxplot_all(AS1_n2, 'AS1 - n2 - g.ext.nic.fr')
# create_boxplot_all(AS1_n3, 'AS1 - n3 - f.ext.nic.fr')
# create_boxplot_all(AS1_r1, 'AS1 - r1 - bcn')
# create_boxplot_all(AS1_r2, 'AS1 - r2 - mnl')
# create_boxplot_all(AS1_r3, 'AS1 - r3 - hnl')
# create_boxplot_all(AS1_i1, 'AS1 - i1 - ok1')
# create_boxplot_all(AS1_i2, 'AS1 - i2 - sgp1')


def create_pdf_plot(dataframe, title, uplim=50):
    dataframe = dataframe[dataframe != float('inf')]
    dataframe = dataframe[dataframe != float('NaN')]
    plt.figure(figsize=(6, 6))
    dataframe.plot.kde()
    plt.title('PDF Plot - ' + title)
    plt.xlabel('RTT Values')
    plt.ylabel('Density')
    plt.xlim(0, uplim)
    plt.savefig(own_path + '\\pdf-plots\\' + title + '.png')
    plt.show()

def create_cdf_plot(dataframe, title):
    dataframe = dataframe[dataframe != float('inf')]
    dataframe = dataframe[dataframe != float('NaN')]
    plt.figure(figsize=(6, 6))
    dataframe.hist(cumulative=True, density=1, bins=100)
    plt.title('CDF Plot - ' + title)
    plt.xlabel('RTT Values')
    plt.ylabel('Density')
    plt.savefig(own_path + '\\cdf-plots\\' + title + '.png')
    plt.show()

# create_pdf_plot(AS1_d1['RTT Avg (ms)'], 'AS1 - d1 - e.ext.nic.fr')
# create_pdf_plot(AS1_d2['RTT Avg (ms)'], 'AS1 - d2 - g.ext.nic.fr')
# create_pdf_plot(AS1_d3['RTT Avg (ms)'], 'AS1 - d3 - f.ext.nic.fr')
# create_pdf_plot(AS1_n1['Total Latency'], 'AS1 - n1 - e.ext.nic.fr')
# create_pdf_plot(AS1_n2['Total Latency'], 'AS1 - n2 - g.ext.nic.fr')
# create_pdf_plot(AS1_n3['Total Latency'], 'AS1 - n3 - f.ext.nic.fr')
# create_pdf_plot(AS1_r1['RTT Avg (ms)'], 'AS1 - r1 - bcn',uplim=100)
# create_pdf_plot(AS1_r2['RTT Avg (ms)'], 'AS1 - r2 - mnl',uplim=500)
# create_pdf_plot(AS1_r3['RTT Avg (ms)'], 'AS1 - r3 - hnl',uplim=500)
# create_pdf_plot(AS1_i1['RTT Avg (ms)'], 'AS1 - i1 - ok1')
# create_pdf_plot(AS1_i2['RTT Avg (ms)'], 'AS1 - i2 - sgp1',uplim=500)

# create_cdf_plot(AS1_d1['RTT Avg (ms)'], 'AS1 - d1 - e.ext.nic.fr')
# create_cdf_plot(AS1_d2['RTT Avg (ms)'], 'AS1 - d2 - g.ext.nic.fr')
# create_cdf_plot(AS1_d3['RTT Avg (ms)'], 'AS1 - d3 - f.ext.nic.fr')
# create_cdf_plot(AS1_n1['Total Latency'], 'AS1 - n1 - e.ext.nic.fr')
# create_cdf_plot(AS1_n2['Total Latency'], 'AS1 - n2 - g.ext.nic.fr')
# create_cdf_plot(AS1_n3['Total Latency'], 'AS1 - n3 - f.ext.nic.fr')
# create_cdf_plot(AS1_r1['RTT Avg (ms)'], 'AS1 - r1 - bcn')
# create_cdf_plot(AS1_r2['RTT Avg (ms)'], 'AS1 - r2 - mnl')
# create_cdf_plot(AS1_r3['RTT Avg (ms)'], 'AS1 - r3 - hnl')
# create_cdf_plot(AS1_i1['RTT Avg (ms)'], 'AS1 - i1 - ok1')
# create_cdf_plot(AS1_i2['RTT Avg (ms)'], 'AS1 - i2 - sgp1')

## All time series
plt.figure(figsize=(14, 6))
plt.grid()
# plt.scatter(AS1_d1['Timestamp'], AS1_d1['RTT Avg (ms)'], label='AS1 - d1 - e.ext.nic.fr', marker='x')
# plt.scatter(AS1_d2['Timestamp'], AS1_d2['RTT Avg (ms)'], label='AS1 - d2 - g.ext.nic.fr', marker='x')
# plt.scatter(AS1_d3['Timestamp'], AS1_d3['RTT Avg (ms)'], label='AS1 - d3 - f.ext.nic.fr', marker='x')
plt.scatter(AS1_n1['Timestamp'], AS1_n1['Total Latency'], label='AS1 - n1 - e.ext.nic.fr', marker='x')
plt.scatter(AS1_n2['Timestamp'], AS1_n2['Total Latency'], label='AS1 - n2 - g.ext.nic.fr', marker='x')
plt.scatter(AS1_n3['Timestamp'], AS1_n3['Total Latency'], label='AS1 - n3 - f.ext.nic.fr', marker='x')
# plt.scatter(AS1_r1['Timestamp'], AS1_r1['RTT Avg (ms)'], label='AS1 - r1 - bcn', marker='x')
# plt.scatter(AS1_r2['Timestamp'], AS1_r2['RTT Avg (ms)'], label='AS1 - r2 - mnl', marker='x')
# plt.scatter(AS1_r3['Timestamp'], AS1_r3['RTT Avg (ms)'], label='AS1 - r3 - hnl', marker='x')
# plt.scatter(AS1_i1['Timestamp'], AS1_i1['RTT Avg (ms)'], label='AS1 - i1 - ok1', marker='x')
# plt.scatter(AS1_i2['Timestamp'], AS1_i2['RTT Avg (ms)'], label='AS1 - i2 - sgp1', marker='x')
plt.title('RTT Avg (ms) - AS1.nX')
plt.xlabel('Timestamp')
plt.ylabel('Total Latency (ms)')
plt.legend()
plt.xticks(np.arange(350,step=20),rotation=20) # For Nameservers!
# plt.xticks(np.arange(2000,step=100),rotation=20) # For Research and Iperf!
plt.savefig(own_path + '\\timeseries\\' + 'AS1.nX' + '.png')
plt.show()

## TABLE DATA
def table_data(dataframe, title):
    dataframe = dataframe[dataframe != float('inf')]
    dataframe = dataframe[dataframe != float('NaN')]
    print(title)
    try:
        print('First delay: ' + str(dataframe[0]))
    except:
        print('First delay: ' + str(dataframe.iloc[0]))
    print('Mean: ' + str(dataframe.mean()))
    print('Median: ' + str(dataframe.median()))
    max_delay = dataframe.mean()*1.5
    proportion_max = dataframe[dataframe > max_delay].count()/dataframe.count()
    print('Percentage of values above 1.5*mean: ' + str(proportion_max*100) + '%')
    distance_quantiles = dataframe.quantile(0.95) - dataframe.quantile(0.5)
    print('Distance between 95th and 50th percentile: ' + str(distance_quantiles))
    print('')


table_data(AS1_d1['RTT Avg (ms)'], 'AS1 - d1 - e.ext.nic.fr')
table_data(AS1_d2['RTT Avg (ms)'], 'AS1 - d2 - g.ext.nic.fr')
table_data(AS1_d3['RTT Avg (ms)'], 'AS1 - d3 - f.ext.nic.fr')
table_data(AS1_n1['Total Latency'], 'AS1 - n1 - e.ext.nic.fr')
table_data(AS1_n2['Total Latency'], 'AS1 - n2 - g.ext.nic.fr')
table_data(AS1_n3['Total Latency'], 'AS1 - n3 - f.ext.nic.fr')
table_data(AS1_r1['RTT Avg (ms)'], 'AS1 - r1 - bcn')
table_data(AS1_r2['RTT Avg (ms)'], 'AS1 - r2 - mnl')
table_data(AS1_r3['RTT Avg (ms)'], 'AS1 - r3 - hnl')
table_data(AS1_i1['RTT Avg (ms)'], 'AS1 - i1 - ok1')
table_data(AS1_i2['RTT Avg (ms)'], 'AS1 - i2 - sgp1')

## Autocorrelation plots

def plot_autocorrelation(dataframe, title):
    dataframe = dataframe[dataframe != float('inf')]
    dataframe = dataframe[dataframe != float('NaN')]
    plt.figure(figsize=(6, 6))
    pd.plotting.autocorrelation_plot(dataframe)
    plt.title('Autocorrelation Plot - ' + title)
    plt.xlabel('Lag')
    plt.ylabel('Autocorrelation')
    plt.savefig(own_path + '\\autocorrelation-plots\\' + title + '.png')
    plt.show()

# plot_autocorrelation(AS1_i1['RTT Avg (ms)'], 'AS1 - i1 - ok1')
# plot_autocorrelation(AS1_i2['RTT Avg (ms)'], 'AS1 - i2 - sgp1')
# plot_autocorrelation(AS1_r1['RTT Avg (ms)'], 'AS1 - r1 - bcn')
# plot_autocorrelation(AS1_d1['RTT Avg (ms)'], 'AS1 - d1 - e.ext.nic.fr')






