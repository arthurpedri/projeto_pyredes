#!/usr/bin/env python

import socket
import sys
from threading import Thread
import time

class Hosts:
    def __init__(self, name, id):
        self.name = name
        self.id = id

def novoLider(hosts):
    menor = hosts[0].id
    for host in hosts:
        if host.id < menor:
            menor = host.id
    return menor

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
    print "Parametros errados:<N> <ID(local)> <host> <id> <host> <id> ...."
    exit()

n = sys.argv[1]
ID = sys.argv[2]
hosts = list()
for i in range(3, len(sys.argv),2):
    h = Hosts(sys.argv[i], sys.argv[i + 1])
    hosts.append(h)
    print i
lider = 0
for host in hosts:
    if host.id < lider:
        lider = host.id

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

        if s.connect_ex((host.name, TCP_PORT)):
            print host.name, " Desconectado"
            m = host.name + " Perdeu Conexao MSG DE: " + ID + " h " + host.id + " l " + str(lider)
            if int (host.id) == int (lider):
                hosts.remove(host)
                lider = novoLider(hosts)
                mLider = "Novo lider e: " + lider + "MSG DE: " + ID
                for remaining in hosts:
                    s.connect_ex((remaining.name, TCP_PORT))
                    s.send(mLider, socket.MSG_OOB)
                    s.close()
            else:
                hosts.remove(host)
                for remaining in hosts:
                    s.connect_ex((remaining.name, TCP_PORT))
                    s.send(m)
                    s.close()
            break
        s.send(MESSAGE)
        s.close()
