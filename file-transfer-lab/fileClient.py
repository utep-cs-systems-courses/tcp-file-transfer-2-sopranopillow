#! /usr/bin/env python3

import sys
sys.path.append("../lib")
sys.path.append("../framed-echo")
import params, socket, re, os
from framedSock import framedSend, framedReceive

switchesVarDefaults = (
    (('-s', '--server'), 'server', '127.0.0.1:50001'),
    (('-d', '--debug'), 'debug', False),
    (('-?', '--usage'), 'usage', False),
    (('-p', '--proxy'), 'proxy', False),
)

def destroyParams(server, debug, usage, proxy): return server, debug, usage, proxy # destructing params

def help():
    print('The following are the available commands:')
    print('\thelp -- show this menu')
    print('\tput <source file> <destination file> -- send file to server')
    print('\texit -- exit program')


def sendFile(sock, source, destination, debug, proxy):
    if not os.path.exists(source):
        print('File %s does not exist' % source)
        return
    f = open(source)
    for line in f:
        payload = "{}:{}".format(destination, line).encode()
        framedSend(sock, payload, debug)
        callback = framedReceive(sock, debug)
    f.close()
    framedSend(sock, b'', debug)
    print(framedReceive(sock, debug).decode())


server, debug, usage, proxy = destroyParams(**params.parseParams(switchesVarDefaults))

if usage: params.usage()

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

while True:
    command = input('$ ')
    if command == 'exit':
        sys.exit(0)
    elif command == 'help':
        help()
    else:
        put = command.split(' ')
        if len(put) != 3:
            print("Wrong use of command, use 'help' command for more info")
        else:
            sendFile(sock, put[1], put[2], debug, proxy)
