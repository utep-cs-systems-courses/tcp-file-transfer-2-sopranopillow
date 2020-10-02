#! /usr/bin/env python3

import sys
sys.path.append("../lib")
sys.path.append("../framed-echo")
import params, socket, re
from framedSock import framedSend, framedReceive

switchesVarDefaults = (
    (('-s', '--server'), 'server', '127.0.0.1:50001'),
    (('-d', '--debug'), 'debug', False),
    (('-?', '--usage'), 'usage', False),
)

def destroyParams(server, debug, usage): return server, debug, usage # destructing params

server, debug, usage = destroyParams(**params.parseParams(switchesVarDefaults))

if usage: params.usage()

try:
    serverHost, serverPort = re.split(':', server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

# ask for file
# validate file
# transfer file
# notify status


addrPort = (serverHost, serverPort)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

if sock is None:
    print('could not open socket')
    sys.exit(1)

sock.connect(addrPort)


