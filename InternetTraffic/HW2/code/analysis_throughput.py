# File analysis_throughput.py
# Aitor Urruticoechea Puig - 2023

import pandas as pd
from datetime import datetime
import os
import numpy as np
import json
from fnmatch import fnmatch
import re
from matplotlib import pyplot as plt
import matplotlib.ticker as plticker

## PATHS

own_path = os.path.dirname(os.path.abspath(__file__))
method1_path = own_path + "/24hlog/throughput-log/method1.csv"
method2_path = own_path + "/24hlog/throughput-log/"
method3_path = own_path + "/24hlog/throughput-log/method3.txt"

## METHOD 1
# Some data cleaning is needed due to the structure of the .csv file
columnames_method1 = ['Timestamp', 'Server', 'Http Code', 'Download Speed (bps)']
unclean_method1 = pd.read_csv(method1_path, header=None)
def cleaning_method1(row):
    timestamp = row[0]
    ok1_httpcode = row[1]
    ok1_download_speed = row[2]
    spg1_httpcode = row[3]
    spg1_download_speed = row[4]
    
    return [timestamp, 'ok1', ok1_httpcode, ok1_download_speed], [timestamp, 'spg1', spg1_httpcode, spg1_download_speed]
clean_method1 = unclean_method1.apply(cleaning_method1,axis=1)
method1data = pd.DataFrame([item for sublist in clean_method1 for item in sublist], columns=['Timestamp', 'Server', 'Http Code', 'Download Speed (bps)'])
method1data['Timestamp'] = pd.to_datetime(method1data['Timestamp'], unit='s')

method1mean = method1data.groupby('Server')['Download Speed (bps)'].mean()
method1median = method1data.groupby('Server')['Download Speed (bps)'].median()
method1max = method1data.groupby('Server')['Download Speed (bps)'].max()
method1min = method1data.groupby('Server')['Download Speed (bps)'].min()
method1minnozero = method1data.replace(0,np.nan).groupby('Server')['Download Speed (bps)'].min()
method1std = method1data.groupby('Server')['Download Speed (bps)'].std()


## METHOD 2
ok1Nfiles = []
ok1Rfiles = []
sgp1Nfiles = []
sgp1Rfiles = []
for filename in os.listdir(method2_path):
    if fnmatch(filename,f'*ok1N*'):
        ok1Nfiles.append(os.path.join(method2_path, filename))
    if fnmatch(filename,f'*ok1R*'):
        ok1Rfiles.append(os.path.join(method2_path, filename))
    if fnmatch(filename,f'*sgp1N*'):
        sgp1Nfiles.append(os.path.join(method2_path, filename))
    if fnmatch(filename,f'*sgp1R*'):
        sgp1Rfiles.append(os.path.join(method2_path, filename))
ok1Ndata = []
ok1Rdata = []
sgp1Ndata = []
sgp1Rdata = []

for filename in ok1Nfiles:
    with open(filename, "r") as json_file:
        data = json.load(json_file)
        match = re.search(r'ok1N(\d+)\.json', filename)
        timestamp_seconds = int(match.group(1))
        timestamp = datetime.utcfromtimestamp(timestamp_seconds).strftime('%Y-%m-%d %H:%M:%S')
        if "streams" in data["end"] and data["end"]["streams"]:
            sender_bps = data["end"]["streams"][0]["sender"]["bits_per_second"]
            receiver_bps = data["end"]["streams"][0]["receiver"]["bits_per_second"]
        else:
            sender_bps = 0
            receiver_bps = 0
        ok1Ndata.append({"Timestamp": timestamp, "Sender_bps": sender_bps,"Receiver_bps": receiver_bps})

for filename in ok1Rfiles:
    with open(filename, "r") as json_file:
        data = json.load(json_file)
        match = re.search(r'ok1R(\d+)\.json', filename)
        timestamp_seconds = int(match.group(1))
        timestamp = datetime.utcfromtimestamp(timestamp_seconds).strftime('%Y-%m-%d %H:%M:%S')
        if "streams" in data["end"] and data["end"]["streams"]:
            sender_bps = data["end"]["streams"][0]["sender"]["bits_per_second"]
            receiver_bps = data["end"]["streams"][0]["receiver"]["bits_per_second"]
        else:
            sender_bps = 0
            receiver_bps = 0
        ok1Rdata.append({"Timestamp": timestamp, "Sender_bps": sender_bps,"Receiver_bps": receiver_bps})

for filename in sgp1Nfiles:
    with open(filename, "r") as json_file:
        data = json.load(json_file)
        match = re.search(r'sgp1N(\d+)\.json', filename)
        timestamp_seconds = int(match.group(1))
        timestamp = datetime.utcfromtimestamp(timestamp_seconds).strftime('%Y-%m-%d %H:%M:%S')
        if "streams" in data["end"] and data["end"]["streams"]:
            sender_bps = data["end"]["streams"][0]["sender"]["bits_per_second"]
            receiver_bps = data["end"]["streams"][0]["receiver"]["bits_per_second"]
        else:
            sender_bps = 0
            receiver_bps = 0
        sgp1Ndata.append({"Timestamp": timestamp, "Sender_bps": sender_bps,"Receiver_bps": receiver_bps})

for filename in sgp1Rfiles:
    with open(filename, "r") as json_file:
        data = json.load(json_file)
        match = re.search(r'sgp1R(\d+)\.json', filename)
        timestamp_seconds = int(match.group(1))
        timestamp = datetime.utcfromtimestamp(timestamp_seconds).strftime('%Y-%m-%d %H:%M:%S')
        if "streams" in data["end"] and data["end"]["streams"]:
            sender_bps = data["end"]["streams"][0]["sender"]["bits_per_second"]
            receiver_bps = data["end"]["streams"][0]["receiver"]["bits_per_second"]
        else:
            sender_bps = 0
            receiver_bps = 0
        sgp1Rdata.append({"Timestamp": timestamp, "Sender_bps": sender_bps,"Receiver_bps": receiver_bps})


ok1Ndata = (pd.DataFrame(ok1Ndata)).sort_values(by='Timestamp').reset_index(drop=True)
ok1Rdata = (pd.DataFrame(ok1Rdata)).sort_values(by='Timestamp').reset_index(drop=True)
sgp1Ndata = (pd.DataFrame(sgp1Ndata)).sort_values(by='Timestamp').reset_index(drop=True)
sgp1Rdata = (pd.DataFrame(sgp1Rdata)).sort_values(by='Timestamp').reset_index(drop=True)

ok1Nmean = ok1Ndata['Sender_bps'].mean()
ok1Nmedian = ok1Ndata['Sender_bps'].median()
ok1Nmax = ok1Ndata['Sender_bps'].max()
ok1Nmin = ok1Ndata['Sender_bps'].min()
ok1Nminnozero = ok1Ndata['Sender_bps'].replace(0,np.nan).min()
ok1Nstd = ok1Ndata['Sender_bps'].std()

ok1Rmean = ok1Rdata['Sender_bps'].mean()
ok1Rmedian = ok1Rdata['Sender_bps'].median()
ok1Rmax = ok1Rdata['Sender_bps'].max()
ok1Rmin = ok1Rdata['Sender_bps'].min()
ok1Rminnozero = ok1Rdata['Sender_bps'].replace(0,np.nan).min()
ok1Rstd = ok1Rdata['Sender_bps'].std()

sgp1Nmean = sgp1Ndata['Sender_bps'].mean()
sgp1Nmedian = sgp1Ndata['Sender_bps'].median()
sgp1Nmax = sgp1Ndata['Sender_bps'].max()
sgp1Nmin = sgp1Ndata['Sender_bps'].min()
sgp1Nminnozero = sgp1Ndata['Sender_bps'].replace(0,np.nan).min()
sgp1Nstd = sgp1Ndata['Sender_bps'].std()

sgp1Rmean = sgp1Rdata['Sender_bps'].mean()
sgp1Rmedian = sgp1Rdata['Sender_bps'].median()
sgp1Rmax = sgp1Rdata['Sender_bps'].max()
sgp1Rmin = sgp1Rdata['Sender_bps'].min()
sgp1Rminnozero = sgp1Rdata['Sender_bps'].replace(0,np.nan).min()
sgp1Rstd = sgp1Rdata['Sender_bps'].std()


## METHOD 3
m3data = pd.read_csv(method3_path, delimiter=' ', header=0)
m3data['Timestamp'] = pd.to_datetime(m3data['Timestamp'], format='%Y%m%d%H%M%S')

m3Nmean = m3data['download'].mean()
m3Nmedian = m3data['download'].median()
m3Nmax = m3data['download'].max()
m3Nmin = m3data['download'].min()
m3Nstd = m3data['download'].std()

m3Rmean = m3data['upload'].mean()
m3Rmedian = m3data['upload'].median()
m3Rmax = m3data['upload'].max()
m3Rmin = m3data['upload'].min()
m3Rstd = m3data['upload'].std()


fig, ax = plt.subplots()
# ax.plot(ok1Ndata['Timestamp'], ok1Ndata['Sender_bps'], label='Method 2: ok1 Normal Ops.')
# ax.plot(ok1Rdata['Timestamp'], ok1Rdata['Sender_bps'], label='Method 2: ok1 Reverse Ops.')
# ax.plot(sgp1Ndata['Timestamp'], sgp1Ndata['Sender_bps'], label='Method 2: sgp1 Normal Ops.')
# ax.plot(sgp1Rdata['Timestamp'], sgp1Rdata['Sender_bps'], label='Method 2: sgp1 Reverse Ops.')
loc = plticker.MultipleLocator(base=8.2)
ax.xaxis.set_major_locator(loc)
plt.xlabel("Timestamp")
plt.ylabel("Throughput (bps)")
plt.legend()
plt.show()
