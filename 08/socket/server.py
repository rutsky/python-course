# Echo server program
import socket
import sys

HOST = None               # Symbolic name meaning all available interfaces
PORT = 50007              # Arbitrary non-privileged port
s = None
interfaces = socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC, 
    socket.SOCK_STREAM, 0, socket.AI_PASSIVE)

af, socktype, proto, canonname, sa = interfaces[0]
s = socket.socket(af, socktype, proto)
s.bind(sa)
s.listen(1)

if s is None:
    print 'could not open socket'
    sys.exit(1)
conn, addr = s.accept()
print 'Connected by', addr
while 1:
    data = conn.recv(1024)
    if not data: break
    conn.send(data)
conn.close()
