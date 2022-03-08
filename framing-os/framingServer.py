#! /usr/bin/env python3

# framing server program

import socket
import sys
import re
import os
import time

import message_handler

sys.path.append("../lib")  # for params
import params

switchesVarDefaults = (
    (('-l', '--listenPort'), 'listenPort', 50001),
    (('-?', '--usage'), "usage", False),  # boolean (set if present)
)

progname = "framingserver"
paramMap = params.parseParams(switchesVarDefaults)

listenPort = paramMap['listenPort']
listenAddr = ''  # Symbolic name meaning all available interfaces

if paramMap['usage']:
    params.usage()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((listenAddr, listenPort))
s.listen(1)  # allow only one outstanding request
# s is a factory for connected sockets

while True:
    conn, addr = s.accept() # wait until incoming connection request (and accept it)
    if os.fork() == 0:      # child becomes server
        print('Connected by', addr)

        os.write(1, 'Enter your Message: \n'.encode())
        message = os.read(1, 1000).decode()
        message_handler.send_message(conn, message)
        conn.shutdown(socket.SHUT_WR)
