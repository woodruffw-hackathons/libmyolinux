#!/usr/bin/env python
# accept-myo-data.py

import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('', 6969))
sock.listen(1)
conn, addr = sock.accept()

while 1:
    data = conn.recv(1024)
    if not data: break
    print data
conn.close()
