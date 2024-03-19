# File AS2analysis.py
# Aitor Urruticoechea Puig - 2023

import pandas as pd
from datetime import datetime
import os
import numpy as np
import json
from fnmatch import fnmatch
import re
from matplotlib import pyplot as plt

## PATHS
own_path = os.path.dirname(os.path.abspath(__file__))
log_path = own_path + "/throughput-log/"

## Reading JSON files
ok1Nfiles = []
ok1Rfiles = []
sgp1Nfiles = []
sgp1Rfiles = []
for filename in os.listdir(log_path):
    if fnmatch(filename,f'*ok1N*'):
        ok1Nfiles.append(os.path.join(log_path, filename))
    if fnmatch(filename,f'*ok1R*'):
        ok1Rfiles.append(os.path.join(log_path, filename))
    if fnmatch(filename,f'*sgp1N*'):
        sgp1Nfiles.append(os.path.join(log_path, filename))
    if fnmatch(filename,f'*sgp1R*'):
        sgp1Rfiles.append(os.path.join(log_path, filename))
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


ok1Ndata = pd.DataFrame(ok1Ndata)
ok1Rdata = pd.DataFrame(ok1Rdata)
sgp1Ndata = pd.DataFrame(sgp1Ndata)
sgp1Rdata = pd.DataFrame(sgp1Rdata)

ok1Ndata['Mode'] = 'N'
ok1Rdata['Mode'] = 'R'
sgp1Ndata['Mode'] = 'N'
sgp1Rdata['Mode'] = 'R'

AS2_i1 = pd.concat([ok1Ndata, ok1Rdata])
AS2_i2 = pd.concat([sgp1Ndata, sgp1Rdata])

AS2_i1 = AS2_i1.sort_values(by='Timestamp').reset_index(drop=True)
AS2_i2 = AS2_i2.sort_values(by='Timestamp').reset_index(drop=True)

## Statistics

def boxplot(data, title): 
    N = data[data["Mode"] == "N"]
    R = data[data["Mode"] == "R"]
    plt.boxplot([N["Sender_bps"], R["Sender_bps"]], labels=["Normal", "Reverse"])
    plt.ylabel("Throughput (bps)")
    plt.yscale("log")
    plt.grid()
    plt.title(title)
    plt.show()

def statistics_analysis(data):
    non_zero_data = [x for x in data if x != 0 and x != float('inf') and x != float('NaN')]
    mean = np.mean(non_zero_data)
    harmonic_mean = len(non_zero_data) / sum([1 / x for x in non_zero_data])
    log_sum = sum(np.log(non_zero_data))
    geometric_mean = np.exp(log_sum / len(non_zero_data))
    median = np.median(non_zero_data)
    print(f"Mean: {mean}, Harmonic Mean: {harmonic_mean}, Geometric Mean: {geometric_mean}, Median: {median}")
    return mean, harmonic_mean, geometric_mean, median

def plot_throughput(data, title):
    plt.scatter(data["Timestamp"], data["Sender_bps"], label="Throughput", marker='x')
    plt.xticks(np.arange(350,step=40),rotation=20)
    plt.xlabel("Timestamp")
    plt.ylabel("Throughput (bps)")
    plt.yscale("log")
    plt.title(title)
    plt.show()  

def plot_autocorrelation(dataframe, title):
    dataframe = dataframe["Sender_bps"]
    dataframe = dataframe[dataframe != float('inf')]
    dataframe = dataframe[dataframe != float('NaN')]
    plt.figure(figsize=(6, 6))
    pd.plotting.autocorrelation_plot(dataframe)
    plt.title('Autocorrelation Plot - ' + title)
    plt.xlabel('Lag')
    plt.ylabel('Autocorrelation')
    plt.show()

# boxplot(AS2_i1, "AS2_i1 - ok1")
# boxplot(AS2_i2, "AS2_i2 - sgp1")
print("AS2_i1 - ok1 - Normal")
statistics_analysis(AS2_i1[AS2_i1["Mode"] == "N"]["Sender_bps"])
print("AS2_i1 - ok1 - Reverse")
statistics_analysis(AS2_i1[AS2_i1["Mode"] == "R"]["Sender_bps"])
print("AS2_i2 - sgp1 - Normal")
statistics_analysis(AS2_i2[AS2_i2["Mode"] == "N"]["Sender_bps"])
print("AS2_i2 - sgp1 - Reverse")
statistics_analysis(AS2_i2[AS2_i2["Mode"] == "R"]["Sender_bps"])
# plot_throughput(AS2_i1[AS2_i1["Mode"] == "N"], "AS2_i1 - ok1 - Normal")
# plot_throughput(AS2_i1[AS2_i1["Mode"] == "R"], "AS2_i1 - ok1 - Reverse")
# plot_throughput(AS2_i2[AS2_i2["Mode"] == "N"], "AS2_i2 - sgp1 - Normal")
# plot_throughput(AS2_i2[AS2_i2["Mode"] == "R"], "AS2_i2 - sgp1 - Reverse")
# plot_autocorrelation(AS2_i1[AS2_i1["Mode"] == "N"], "AS2_i1 - ok1 - Normal")
# plot_autocorrelation(AS2_i1[AS2_i1["Mode"] == "R"], "AS2_i1 - ok1 - Reverse")
# plot_autocorrelation(AS2_i2[AS2_i2["Mode"] == "N"], "AS2_i2 - sgp1 - Normal")
# plot_autocorrelation(AS2_i2[AS2_i2["Mode"] == "R"], "AS2_i2 - sgp1 - Reverse")
