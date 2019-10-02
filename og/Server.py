#!/usr/bin/python3

# Import socket module
from socket import *
import sys
import string

# Create a TCP server socket
#(AF_INET is used for IPv4 protocols)
#(SOCK_STREAM is used for TCP)




def checkGet(inp):
    """
    Checks that the first token is equal
    to 'GET' exactly!
    """

    get = "GET"
    out = True
    if len(inp) != 3:
        out = False
    if inp != get:
        out = False
    return out


def checkURL(inp):
    """
    Makes sure that the second token begins with a '/',
    and does not contain any not allowed characters.
    """

    out = True
    if inp[0] != "/":
        out = False
    charsAllowed=(string.ascii_lowercase + string.ascii_uppercase + string.digits + "." + "_" + "/")
    for z in inp:
        if z not in charsAllowed:
            out = False
    return out


def checkHTTP(inp):
    """
    Makes sure that the third token is in the form:
    'HTTP/#.#'.
    """

    try:
        out = True
        if len(inp) != 8:
            out = False
        if inp[0:4] != "HTTP":
            out = False
        if inp[4] != "/":
            out = False
        if inp[5] not in string.digits:
            out = False
        if inp[6] != ".":
            out = False
        if inp[7] not in string.digits:
            out = False
        return out
    except Exception:
        out= False
    return out


def checkSpurious(inp):
    """
    Checks to make sure that there aren't four tokens,
    meaning there is random text after the third.
    """

    if len(inp) >= 4:
        return True
    else:
        return False


def passedFunctions(inp):
    """
    This function is called when all other tests are passed.
    It checks to see if the URL ends in a recognized string,
    and tries to open them. If it can't, it throws errors
    based on why not.
    """

    if inp.endswith((".htm", ".txt", ".html", ".HTM", ".TXT", ".HTML")):
        try:
            in_file = open(inp[1:], "r")
            text = in_file.readlines()
            for l in text:
                print(l[:len(l)-1])
        except FileNotFoundError:
            print("404 Not Found: " + inp)
        except IOError:
            print(IOError)
    else:
        print("501 Not Implemented: " + inp)


def main(new):
    """
    The main function which loops through all lines of input,
    and splits the input into lists by whitespace. It then calls
    the functions to test the tokens in the input, and prints the
    results.
    """
    sys.stdout = open('memory.txt', 'wt')

    stop = True
    while stop:
        new = ''.join(new)

        method = ""
        request_url = ""
        HTTP_version = ""
        print(new, end = "")
        # tab case
        if new.find("\t") > 2:
            new = new.split("\t")

        # catching the case where there is a space in the Get thing.
        if new[0] == " ":
            print("ERROR -- Invalid Method token.")
            stop = False
        # base space case
        new = new.split()
        try:
            method = new[0]
            request_url = new[1]
            HTTP_version = new[2]
        except Exception:
            pass

        if (len(new) == 0) or ((checkGet(method)) == False):
            print("ERROR -- Invalid Method token.")
        elif (len(new) == 1) or ((checkURL(request_url)) == False):
            print("ERROR -- Invalid Absolute-Path token.")
        elif (len(new) == 2) or ((checkHTTP(HTTP_version)) == False):
            print("ERROR -- Invalid HTTP-Version token.")
        elif (checkSpurious(new)):
            print("ERROR -- Spurious token before CRLF.")
        else:
            print("Method = " + method)
            print("Request-URL = " + request_url)
            print("HTTP-Version = " + HTTP_version)
            passedFunctions(request_url)
        stop = False

#####################################
# This is the main function!!!!!!!! #
#####################################


serverSocket = socket(AF_INET, SOCK_STREAM)

# Assign a port number
serverPort = int(sys.argv[1])

# Bind the socket to server address (default this machine)
# and server port
try:
    serverSocket.bind(("", serverPort))
except (OSError):
    print("Connection Error")
    sys.exit()

# Listen for at most 1 connection at a time
serverSocket.listen(1)

# Server should be up and running first,
# and listening to the incoming connections

while True:
    sys.stdout = open('memory.txt', 'wt')
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
    # messageCaps = message.upper()
    main(message)

    # Send back to client
    saved = open("memory.txt", "r")
    sys.stdout = sys.__stdout__
    lines = saved.readlines()
    s.write(str(len(lines)) + "\n")
    for x in lines:
        s.write(x)
    s.flush()

    # Close the client connection socket
    connectionSocket.close()

serverSocket.close()
sys.exit()#Terminate the program after sending the corresponding data





