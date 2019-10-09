###############################################################
#  This code by Ian Ferguson - 10.8.2019                      #
###############################################################

import sys
from socket import *

# Take in the port from sys.argv
port = sys.argv[1]

# take in the input from stdin.
lines = sys.stdin.readlines()

for line in lines:
    if len(line) == 0:
        pass


# client creates a new socket and connection for each
# request/response exchange with the server
# Create a TCP server socket
# (AF_INET is used for IPv4 protocols)
# (SOCK_STREAM is used for TCP)

    clientSocket = socket(AF_INET, SOCK_STREAM)
    hostPort = int(port)
    host_name = "comp431afa19.cs.unc.edu"

# Connect to the specified host and port

    clientSocket.connect((host_name,hostPort))

# Make a bidirectional stream (file-like) from socket
# read and write operations can be used on the stream

    s = clientSocket.makefile("rw")

# write input line to server over the connection
    s.write(line)
    s.flush()

# read the server response line
    # get the amount of lines to read.
    count = (s.readline())
    # add carriage return to the first line.
    first = s.readline()
    first = first.replace("\n", "\r")
    print(first)
    # loop through the rest using the first
    # line, which was count, and print
    for x in range(int(count)-1):
        y = s.readline()
        y = y.replace("\n", "")
        if (y != " ") and (y != "\n") and (y != " "):
            print(y)

# close the connection after each request/response
    clientSocket.close()
