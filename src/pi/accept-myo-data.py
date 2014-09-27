#!/usr/bin/env python
# accept-myo-data.py

import socket
import struct

POSES = {
0 : "rest",
1 : "fist",
2 : "waveIn",
3 : "waveOut",
4 : "fingersSpread",
5 : "reserved1",
6 : "thumbToPinky",
}

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('', 6969))
sock.listen(1)
conn, addr = sock.accept()

while 1:
    data = struct.unpack("fffffffBB", conn.recv(30))
    motion = POSES.get(conn[7], 'unknown')
    if not data: break
    print data
conn.close()
