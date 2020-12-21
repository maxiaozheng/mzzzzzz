"""
IO多路复用演示 poll
"""
from socket import *
from select import *

tcp_sock = socket()
tcp_sock.bind(('0.0.0.0', 8888))
tcp_sock.listen(5)

tcp_sock.setblocking(False)

p = poll()
p.register(tcp_sock, POLLIN)
print("开始监控")
map = {tcp_sock.fileno(): tcp_sock}

while True:
    events = p.poll()
    print("就绪的IO：", events)
    for fd, event in events:
        if fd == tcp_sock.fileno():
            connfd, addr = map[fd].accept()
            print("Connect from", addr)
            map[connfd.fileno()] = connfd
            p.register(connfd, POLLIN)
        else:
            data = map[fd].recv(1024)
            if not data:
                p.unregister(fd)
                map[fd].close()
                del map[fd]
                continue
            print(data.decode())
            map[fd].send(b"OK")
