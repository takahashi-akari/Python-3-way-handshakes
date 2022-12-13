"""
This is a simple example of a Python script that can be used to 3-way handshake
with a server. This is useful for testing the server's ability to handle
connections.

@author: Takahashi Akari
@date: 2022/12/13
"""

import random
from scapy.all import *

sport = random.randint(30000,60000)
seq = random.randint(1000,2000)
ip = IP(dst=input('Enter the IP address of the server: '))
tcp = TCP(sport=sport, dport=input('Enter the port number of the server: '), flags='S', seq=seq)

syn = ip/tcp
syn_ack = sr1(syn)

tcp.seq = syn_ack.ack
tcp.ack = syn_ack.seq + 1
tcp.flags = 'A'
ack = ip/tcp
send(ack)