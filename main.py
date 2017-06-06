#!/usr/bin/env python

import socket
import sys
from threading import Thread
import time
import datetime

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

def listener(n, id): # funcao aberta com thread para escutar a porta 5005
    TCP_IP = ''
    TCP_PORT = 5005
    BUFFER_SIZE = 1024

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # abrindo socket
    s.bind((TCP_IP, TCP_PORT))
    s.listen(int(n)) # especificando a quantidade de peers para se conectarem

    while 1:
        conn, addr = s.accept() # aceita uma conexao tcp
        # print id, ': Connection address:', addr
        data = conn.recv(BUFFER_SIZE) # coloca o conteudo da mensagem na variavel data
        # if not data: break
        print "[", id, "] [",datetime.datetime.utcnow().strftime("%H:%M:%S"), "]", " >> ", data
        conn.close()


if len(sys.argv) < 2: # verificacao para facil demonstracao de uso do programa
    print "Parametros errados:<N> <ID(local)> <host1> <id1> <host2> <id2> ... <hostN> <idN>"
    exit()

print "============================================================================="
print "Inicio da execucao: programa que implementa peers sobre tcp."
print "Arthur Pedri Trevisol GRR20141784 - Arthur Carvalho de Queiroz GRR20141754"
print "REDES DE COMPUTADORES II"
print "============================================================================="
print

n = sys.argv[1] # numero de hosts
ID = sys.argv[2] # id do host local
hosts = list() # lista de hosts fora o local
for i in range(3, len(sys.argv),2):
    h = Hosts(sys.argv[i], sys.argv[i + 1]) # adicionar um host a lista de hosts com seu nome e id
    hosts.append(h)
    #print i
print "Lista de hosts criada"

t = Thread(target=listener, args=(n,ID,)) # declara a thread que vai usar a funcao listener
t.start() # abre a thread

print "Thread Listener Lancada"

TCP_PORT = 5005
BUFFER_SIZE = 1024
HEARTBEAT = "Heartbeat DE "+ID # determina a mensagem de heartbeat


##ELEICAO

ELEICAO = "ESTADO DE ELEICAO MSG DE " + ID
ALL_UP = False
while not ALL_UP: # enquanto todos os hosts nao estiverem conectados o programa nao vai sair desse while
    ALL_UP = True
    time.sleep(1)
    for host in hosts: # Percorre todos os peers para saber quem realmente esta ativo
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if not s.connect_ex((host.name, TCP_PORT)): # verificar se alguma conexao foi fechada
            s.send(ELEICAO)
            s.close()
        else:
            ALL_UP = False

print "Todos hosts conectados"

lider = novoLider(hosts, ID) # Com a lista atualizada, define o novo lider

print "Lider ID: " + str(lider)

print "Inicio do while do Sender"

while 1:
    for host in hosts:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        time.sleep(1)

        if s.connect_ex((host.name, TCP_PORT)): # verificar se alguma conexao foi fechada
            print host.name, " Desconectado" # avisa o usuario que o host foi desconectado
            m = host.name + " Perdeu Conexao MSG DE: " + ID
            if int (host.id) == int (lider): # ajustes para quando o host desconectado foi o lider
                hosts.remove(host) # remove o desconectado da lista de hosts

                ##ELEICAO
                for elect in hosts: # Percorre todos os peers para saber quem realmente esta ativo
                    if not s.connect_ex((elect.name, TCP_PORT)): # verificar se alguma conexao foi fechada
                        s.send(ELEICAO)
                        s.close()
                    else:
                        hosts.remove(elect) # se alguma outra conexao foi fechada o host sera removido da lista de hosts e ele nao sera candidato a lideranca

                lider = novoLider(hosts, ID) # chama a funcao para definir o novo lider
                mLider = "Novo lider e: " + str(lider) # prepara a mensagem informando quem e o novo lider
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                for remaining in hosts: # manda a mensagem informando quem e o novo lider
                    s.connect_ex((remaining.name, TCP_PORT))
                    s.send(mLider, socket.MSG_OOB) # manda a mensagem informando o novo lider com tag de mensagem urgente
                    s.close()
            else: # caso o host desconectado nao seja o lider so manda mensagem informando o host desconectado
                hosts.remove(host) # remove o host da lista
                for remaining in hosts: # informa aos restantes que o host foi desconectado
                    s.connect_ex((remaining.name, TCP_PORT))
                    s.send(m)
                    s.close()
            break
        s.send(HEARTBEAT) # manda o heartbeat para a rede
        s.close() # fecha o socket
