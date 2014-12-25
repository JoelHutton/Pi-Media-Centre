#!/usr/bin/env python
# Echo client program
import socket
import cgi
print "Content-Type: text/html\r\n\r\n"
print

form = cgi.FieldStorage()
command = raw_input('what is your JSON command?:')
command = command.strip()

udp_ip_source          = "127.0.0.1" #raw_input('what is your ip address?:')
udp_port_source        = 50007
udp_ip_destination     = "127.0.0.1"
udp_port_destination   = 50008
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

send_string = command
sock.bind((udp_ip_source, udp_port_source))
sock.sendto(send_string, (udp_ip_destination, udp_port_destination))
data = sock.recvfrom(1024) # buffer size is 1024 bytes
status = str(data[0])
print status
