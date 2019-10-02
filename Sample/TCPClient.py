#!/usr/bin/python3

import sys
from socket import *

for line in sys.stdin:
    if len(line) == 0:
        break

#client creates a new socket and connection for each
#request/response exchange with the server
# Create a TCP server socket
#(AF_INET is used for IPv4 protocols)
#(SOCK_STREAM is used for TCP)

    clientSocket=socket(AF_INET, SOCK_STREAM)
    hostPort=15382
    host_name = "comp431afa19.cs.unc.edu"

#connect to the specified host and port

    clientSocket.connect((host_name,hostPort))

# Make a bidirectional stream (file-like) from socket
# read and write operations can be used on the stream

    s = clientSocket.makefile("rw")

# write input line to server over the connection
    s.write(line)
    s.flush()

# read the server response line
    lineUC = s.readline()

    sys.stdout.write(lineUC)

# close the connection after each request/response
    clientSocket.close()

sys.exit