#! /usr/bin/env python3

import sys
sys.path.append("../lib")
sys.path.append("../framed-echo")
import re, socket, params, os
from framedSock import framedSend, framedReceive

def destroyParams(debug, listenPort, usage, maxConnections):
    return debug, listenPort, usage, maxConnections # destructing dictionary

switchesVarDefaults = (
    (('-l', '--listenPort'), 'listenPort', 50001),
    (('-d', '--debug'), 'debug', False),
    (('-?', '--usage'), 'usage', False),
    (('-c', '--connections'), 'maxConnections', 5)
)

debug, listenPort, usage, maxConnections = destroyParams(**params.parseParams(switchesVarDefaults))

if usage: params.usage() # printing usage

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
bindAddr = ('127.0.0.1', listenPort)
lsock.bind(bindAddr)
lsock.listen(maxConnections)
print('listening on:',bindAddr)

while True:
    sock, addr = lsock.accept()
    if not os.fork():
        print("new child process handling connection from", addr)
        while True:
            payload = framedReceive(sock, debug)
            if payload == b'':
                break
            if payload != None:
                f, data = re.split(':', payload.decode())
                print('####',f,'\n####',data, data.encode())
                fd = os.open(f, os.O_CREAT | os.O_WRONLY)
                os.write(fd, data.encode())
                os.close(fd)
                if debug: print("rec'd", payload.decode())
                framedSend(sock, 'Successfuly received and wrote line'.encode())
        framedSend(sock, 'File transfered succesfully'.encode())
        print("child from connection {} closed".format(addr))
