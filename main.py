#!/usr/bin/env python

import socket
import sys
from threading import Thread
import time

class Hosts: # Classe para usar na lista de hosts, contendo nome e id
    def __init__(self, name, id):
        self.name = name
        self.id = id

def novoLider(hosts, id): # Funcao para determinar um lider novo com base na lista de hosts e no proprio id
    menor = int(id)
    for host in hosts:
        if int(host.id) < int(menor):
            menor = host.id
    return menor

def listener(n, id):
    TCP_IP = ''
    TCP_PORT = 5005
    BUFFER_SIZE = 1024

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
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

n = sys.argv[1] # numero de hosts
ID = sys.argv[2] # id do host local
hosts = list() # lista de hosts fora o local
for i in range(3, len(sys.argv),2):
    h = Hosts(sys.argv[i], sys.argv[i + 1]) # adicionar um host a lista de hosts com seu nome e id
    hosts.append(h)
    print i

t = Thread(target=listener, args=(n,ID,))
t.start()

# TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024
HEARTBEAT = "Heartbeat from "+ID

time.sleep(5)
##ELEICAO

ELEICAO = "ESTADO DE ELEICAO MSG DE " + ID
ALL_UP = FALSE
while not ALL_UP
    ALL_UP = TRUE
    for host in hosts: # Percorre todos os peers para saber quem realmente esta ativo
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if not s.connect_ex((host.name, TCP_PORT)): # verificar se alguma conexao foi fechada
            s.send(ELEICAO)
            s.close()
        else:
            ALL_UP = FALSE

lider = novoLider(hosts, ID) # Com a lista atualizada, defini o novo lider


while 1:
    for host in hosts:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        time.sleep(1)

        if s.connect_ex((host.name, TCP_PORT)): # verificar se alguma conexao foi fechada
            print host.name, " Desconectado"
            m = host.name + " Perdeu Conexao MSG DE: " + ID
            if int (host.id) == int (lider): # ajustes para quando o host desconectado foi o lider
                hosts.remove(host) # remove o desconectado da lista de hosts

                ##ELEICAO
                for elect in hosts: # Percorre todos os peers para saber quem realmente esta ativo
                    if not s.connect_ex((elect.name, TCP_PORT)): # verificar se alguma conexao foi fechada
                        s.send(ELEICAO)
                        s.close()
                    else:
                        hosts.remove(elect)

                lider = novoLider(hosts, ID) # chama a funcao para definir o novo lider
                mLider = "Novo lider e: " + str(lider) + " MSG DE: " +ID # prepara a mensagem informando quem e o novo lider
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                for remaining in hosts: # manda a mensagem informando quem e o novo lider
                    s.connect_ex((remaining.name, TCP_PORT))
                    s.send(mLider, socket.MSG_OOB)
                    s.close()
            else: # caso o host desconectado nao seja o lider so manda mensagem informando o host desconectado
                hosts.remove(host)
                for remaining in hosts:
                    s.connect_ex((remaining.name, TCP_PORT))
                    s.send(m)
                    s.close()
            break
        s.send(HEARTBEAT)
        s.close()
