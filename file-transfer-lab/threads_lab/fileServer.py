#! /usr/bin/env python3

import sys
sys.path.append("../../lib")
sys.path.append("../../framed-echo")
import socket, params, re, os
from threading import Thread, Lock
from encapFramedSock import EncapFramedSock

switchesVarDefaults = (
    (('-l', '--listenPort'), 'listenPort', 50001),
    (('-d', '--debug'), 'debug', False),
    (('-?', '--usage'), 'usage', False),
    (('-c', '--connections'), 'maxConnections', 5)
)

def destroyParams(debug, listenPort, usage, maxConnections):
    return debug, listenPort, usage, maxConnections # destructing dictionary

currentFile = {} # dictionary needed to tell which file is in use

debug, listenPort, usage, maxConnections = destroyParams(**params.parseParams(switchesVarDefaults))

if usage: params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
bindAddr = ('127.0.0.1', int(listenPort))
lsock.bind(bindAddr)
lsock.listen(maxConnections)
print('listening on:', bindAddr)
lock = Lock()

class Server(Thread):
    def __init__(self, sockAddr):
        Thread.__init__(self)
        self.sock, self.addr = sockAddr
        self.fsock = EncapFramedSock(sockAddr)
    def run(self):
        print("new thread handling connection from", self.addr)

        global lock, currentFile # need to use global keyword because of threads

        while True:
            try:
                payload = self.fsock.receive(debug)

                if payload == b'': # means we've reached end
                    lock.acquire() # Locks is needed in case two threads try to access the dict at the same time
                    de = ""
                    for i in currentFile: # This is needed since we don't know the name of the file
                        if currentFile[i] == self.addr[1]:
                            de = i
                    currentFile.pop(de)
                    lock.release()
                    break
                if payload != None:
                    f, data = re.split(':', payload.decode())
                    if len(currentFile) > 0 and f in currentFile and currentFile[f] != self.addr[1]:
                        print('Failed to send file, file is in use')
                        self.fsock.send(b'abort', debug) # letting client know someone is using the file
                        sys.exit(1)
                    else:
                        if len(currentFile) == 0 or not f in currentFile:
                            fd = open(f, 'w+') # if first time writing to file then create new file
                        else:
                            fd = open(f, 'a+') # otherwise just append
                        lock.acquire()
                        currentFile[f] = self.addr[1] # using addr[1] as the differentiator
                        lock.release()
                    fd.write(data)
                    fd.close()
                    if debug: print("rec'd", payload.decode())
                    self.fsock.send('Successfuly received and wrote line'.encode(), debug)
            except Exception as e:
                print('Exception: Could not finish receiving file\n', e)
                sys.exit(1)
        self.fsock.send('Successfuly received file'.encode(), debug)

if __name__ == "__main__":
    while True:
        sockAddr = lsock.accept()
        server = Server(sockAddr)
        server.start()
    lsock.close()
