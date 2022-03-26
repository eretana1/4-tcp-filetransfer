#! /usr/bin/env python3

# framing server program

import socket
import sys
import re
import os
import time
import _thread as thread

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
s.listen(5)  # allow for multiple outstanding request
# s is a factory for connected sockets
thread_lock = thread.allocate_lock()

while True:
    conn, addr = s.accept() # wait until incoming connection request (and accept it)
    
    #os.fork() generates child process (but does not have shared memory)
    print('Connected by', addr)
    
    os.write(1, f'Sending file: {file_name} \n'.encode())
    thread.start_new_thread(file_handler.send_file, (conn, file_name, thread_lock))
    
conn.shutdown(socket.SHUT_WR)
