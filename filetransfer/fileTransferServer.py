#! /usr/bin/env python3

# framing server program

import socket
import sys
import re
import os
import time

import message_handler
import file_handler

sys.path.append("../lib")  # for params
import params

switchesVarDefaults = (
    (('-l', '--listenPort'), 'listenPort', 50001),
    (('-?', '--usage'), "usage", False),  # boolean (set if present)
)

progname = "framingserver"
#paramMap = params.parseParams(switchesVarDefaults)

listenPort = 50001 #paramMap['listenPort']
listenAddr = ''  # Symbolic name meaning all available interfaces

if '-?' in sys.argv:
    os.write(1, './fileTransferServer.py -f <filename>\n'.encode())

if '-f' in sys.argv:
    file_name = sys.argv[sys.argv.index('-f') + 1]
else:
    file_name = ''
    
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((listenAddr, listenPort))
s.listen(1)  # allow only one outstanding request
# s is a factory for connected sockets

while True:
    conn, addr = s.accept() # wait until incoming connection request (and accept it)
    if os.fork() == 0:      # child becomes server
        print('Connected by', addr)

        os.write(1, f'Sending file: {file_name} \n'.encode())
        file_handler.send_file(conn, file_name)
        conn.shutdown(socket.SHUT_WR)
