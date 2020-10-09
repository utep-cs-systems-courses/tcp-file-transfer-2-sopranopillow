#! /usr/bin/env python3

import sys
sys.path.append("../lib")
sys.path.append("../framed-echo")
import socket, re, os
from framedSock import framedSend, framedReceive

switchesVarDefaults = (
    (('-s', '--server'), 'server', '127.0.0.1:50001'),
    (('-d', '--debug'), 'debug', False),
    (('-?', '--usage'), 'usage', False),
    (('-p', '--proxy'), 'proxy', False)
)

def destroyParams(server, debug, usage, proxy): return server, debug, usage, proxy # destructing params

def sendFile(sock, source, destination, debug, proxy): # Sends file based on source, destination and proxy
    if not os.path.exists(source):
        print('File %s does not exist' % source)
        return
    f = open(source)
    for line in f:
        payload = "{}:{}".format(destination, line).encode()
        framedSend(sock, payload, debug)
        callback = framedReceive(sock, debug)
    f.close()
    framedSend(sock, b'', debug) # Letting server know file transfered completely
    print(framedReceive(sock, debug).decode())

put = False
    
if len(sys.argv) > 1 and 'put' in sys.argv: # Setting up put, source and destination values
    if len(sys.argv) < 3:
        print("Wrong use of command or params, to send a file please use the following notation: ./fileClient.py put <sourceFile> <destinationFile> [params]")
        sys.exit(0)
    putIndex = sys.argv.index('put')
    put, source, destination = True, sys.argv[putIndex + 1], sys.argv[putIndex + 2]
    sys.argv = sys.argv[:putIndex] + (sys.argv[putIndex + 4:] if len(sys.argv) > putIndex + 4 else []) # Resetting argv so that there are no errors when checking for params
    
import params # has to be imported until here since params runs code when imported therefore argv needs to be dealt with before importing.
    
server, debug, usage, proxy = destroyParams(**params.parseParams(switchesVarDefaults))

if usage: params.usage()

if put:
    try:
        serverHost, serverPort = re.split(':', server)
        serverPort = int(serverPort)
    except:
        print("Can't parse server:port from '%s'" % server)
        sys.exit(1)

    addrPort = (serverHost, serverPort)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    if sock is None:
        print('could not open socket')
        sys.exit(1)

    sock.connect(addrPort)

    sendFile(sock, source, destination, debug, proxy)
# assuming that if put is not given then user must have tried --usage
