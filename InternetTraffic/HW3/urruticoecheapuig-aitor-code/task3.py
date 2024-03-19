# File task3.py
# Aitor Urruticoechea 2023

import pandas as pd

filetcp = "task3tcp.csv"
fileudp = "task3udp.csv"
file_convtcp = "task3conversationtcp.csv"

tcp = pd.read_csv(filetcp)
udp = pd.read_csv(fileudp)
tcp_conv = pd.read_csv(file_convtcp)


print(tcp.groupby('Port')['Packets'].sum().sort_values(ascending=False).head(15))
print(udp.groupby('Port')['Packets'].sum().sort_values(ascending=False).head(15))

print(tcp_conv[tcp_conv['Bits/s A → B'] != float('inf')].sort_values(by='Bits/s A → B',ascending=False).head(10))
print(tcp_conv[tcp_conv['Bits/s B → A'] != float('inf')].sort_values(by='Bits/s B → A',ascending=False).head(10))