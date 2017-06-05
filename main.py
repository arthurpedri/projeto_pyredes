#!/usr/bin/env python

import socket
import sys
from threading import Thread
import time


def listener(n, id):
    TCP_IP = ''
    TCP_PORT = 5005
    BUFFER_SIZE = 1024  # Normally 1024, but we want fast response

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    time.sleep(5)
    s.listen(int(n))

    while 1:
        conn, addr = s.accept()
        # print id, ': Connection address:', addr
        data = conn.recv(BUFFER_SIZE)
        # if not data: break
        print id, ": received data:", data
        conn.close()


if len(sys.argv) < 2:
    print "Parametros errados:<N> <ID> <host> <host> ...."
    exit()

n = sys.argv[1]
ID = sys.argv[2]
hosts = list()

for i in range(3,len(sys.argv)):
    hosts.append(sys.argv[i])
    print i
for host in hosts:
    print host

t = Thread(target=listener, args=(n,ID,))
t.start()

# TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024
MESSAGE = "Heartbeat from "+ID

time.sleep(5)
while 1:
    for host in hosts:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        time.sleep(1)

        if s.connect_ex((host, TCP_PORT)):
            print host, " Desconectado"
            hosts.remove(host)
            for remaining in hosts:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect_ex((host, TCP_PORT)
                s.send(host + "Caiu", socket.MSG_OOB)
                s.close()
            break;
        s.send(MESSAGE)
        s.close()
