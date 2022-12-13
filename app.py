"""
This is a simple example of a Python script that can be used to 3-way handshake
with a server. This is useful for testing the server's ability to handle
connections.

@author: Takahashi Akari
@date: 2022/12/13
@version: 0.1
@license: MIT License copyright (c) 2022 Takahashi Akari
"""

import random
from scapy.all import *

def arp_spoof(targetIP, injectIP):
    send(ARP(op='is-at', psrc=injectIP, pdst=targetIP, hwdst="ff:ff:ff:ff:ff:ff"))

fakeIP = input('Enter the fake src IP: ')               # fake src IP address
targetIP = input('Enter the IP address of the server: ')               # target IP address
targetPort = int(input('Enter the port number of the server: '))      # target port number
gwaddr = conf.route.route('0.0.0.0')[2] # target gateway address

### inject IP address to target
t = threading.Timer(0.3, arp_spoof, args=(gwaddr, fakeIP, ))
t.start()
res = sr1(IP(dst=gwaddr, src=fakeIP)/ICMP())
print(res.summary())

### open TCP connection
sport = random.randint(30000,60000)
seq = random.randint(1000,2000)
ip = IP(dst=targetIP, src=fakeIP)
tcp = TCP(sport=sport,dport=targetPort,seq=seq,flags='S')

syn = ip/tcp
syn_ack = sr1(syn)

tcp.seq = syn_ack.ack
tcp.ack = syn_ack.seq + 1
tcp.flags = 'A'
ack = ip/tcp
send(ack)

### INSERT YOUR ACTION HERE


### close TCP connection
tcp.flags = 'FA'
fin_ack = sr1(ip/tcp)

tcp.seq += 1
tcp.ack = fin_ack.seq + 1
tcp.flags = 'A'
send(ip/tcp)