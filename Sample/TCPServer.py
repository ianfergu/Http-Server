#!/usr/bin/python3

# Import socket module
from socket import *
import sys

# Create a TCP server socket
#(AF_INET is used for IPv4 protocols)
#(SOCK_STREAM is used for TCP)

serverSocket = socket(AF_INET, SOCK_STREAM)

# Assign a port number
serverPort = 15382

# Bind the socket to server address (default this machine)
# and server port
serverSocket.bind(("", serverPort))

# Listen for at most 1 connection at a time
serverSocket.listen(1)

# Server should be up and running first,
# and listening to the incoming connections

while True:
    print('The server is ready to receive')

    #Wait for a new connection from the client
    #and accept it when requested
    #a new socket for data streams is returned from
    #the accept method
    connectionSocket, addr = serverSocket.accept()

    # Make a bidirectional stream (file-like) from socket
    # read and write operations can be used on the stream
    s = connectionSocket.makefile("rw")

    # Receives the request message from the client
    message = s.readline()

    # Create upper case version
    messageCaps = message.upper()

    # Send back to client
    s.write(messageCaps)
    s.flush()

    # Close the client connection socket
    connectionSocket.close()

serverSocket.close()
sys.exit()#Terminate the program after sending the corresponding data