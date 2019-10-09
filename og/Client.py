#!/usr/bin/python3


import sys
from socket import *
import string

port = sys.argv[1]


lines = sys.stdin.readlines()

for line in lines:
    if len(line) == 0:
        pass


#client creates a new socket and connection for each
#request/response exchange with the server
# Create a TCP server socket
#(AF_INET is used for IPv4 protocols)
#(SOCK_STREAM is used for TCP)

    clientSocket = socket(AF_INET, SOCK_STREAM)
    hostPort = int(port)
    host_name = "comp431bfa19.cs.unc.edu"

#connect to the specified host and port

    clientSocket.connect((host_name,hostPort))

# Make a bidirectional stream (file-like) from socket
# read and write operations can be used on the stream

    s = clientSocket.makefile("rw")

# write input line to server over the connection
    s.write(line)
    s.flush()

# read the server response line
    """
    lent = int(s.readline())
    first_line = s.readline()
    first_line = first_line.replace("\n" , "\r")
    print(first_line)
    for x in range(lent-1):
        y = s.readline()
        y = y.replace("\n", "")
        if (y != " ") and (y != "\n") and (y != " "):
            print(y) """

    z = s.readline()
    print(z)

# close the connection after each request/response
    clientSocket.close()
