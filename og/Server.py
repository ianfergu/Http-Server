#!/usr/bin/python3

# Import socket module
from socket import *
import sys
import string
import io
import tempfile
from io import StringIO

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


def passedFunctions(inp, output):
    """
    This function is called when all other tests are passed.
    It checks to see if the URL ends in a recognized string,
    and tries to open them. If it can't, it throws errors
    based on why not.
    """
    print(output)
    if inp.endswith((".htm", ".txt", ".html", ".HTM", ".TXT", ".HTML")):
        try:
            in_file = open(inp[1:], "r")
            text = in_file.readlines()
            for l in text:
                output.write((l[:len(l)-1] + "\n").encode('utf-8'))
                # print(l[:len(l)-1])
        except FileNotFoundError:
            # print("404 Not Found: " + inp)
            output.write(("404 Not Found: " + inp + "\n").encode('utf-8'))
        except IOError:
            # print(IOError)
            output.write((IOError + "\n").encode('utf-8'))
    else:
        # print("501 Not Implemented: " + inp)
        output.write(("501 Not Implemented: " + inp + "\n").encode('utf-8'))
    return output


def main(new, output):
    """
    The main function which loops through all lines of input,
    and splits the input into lists by whitespace. It then calls
    the functions to test the tokens in the input, and prints the
    results.
    """
    stop = True
    while stop:
        new = ''.join(new)

        method = ""
        request_url = ""
        HTTP_version = ""
        # print(new, end = "")
        output.write((new + "\r\n"))
        # tab case
        if new.find("\t") > 2:
            new = new.split("\t")

        # catching the case where there is a space in the Get thing.
        if new[0] == " ":
            # print("ERROR -- Invalid Method token.")
            output.write(("ERROR -- Invalid Method token." + '\n').encode('utf-8'))
            stop = False
        # base space case
        new = new.split()
        try:
            method = new[0]
            request_url = new[1]
            HTTP_version = new[2]
        except Exception:
            return output

        if (len(new) == 0) or ((checkGet(method)) == False):
            # print("ERROR -- Invalid Method token.")
            output.write(("ERROR -- Invalid Method token." + "\n").encode('utf-8'))
        elif (len(new) == 1) or ((checkURL(request_url)) == False):
            # print("ERROR -- Invalid Absolute-Path token.")
            output.write(("ERROR -- Invalid Absolute-Path token." + "\n").encode('utf-8'))
        elif (len(new) == 2) or ((checkHTTP(HTTP_version)) == False):
            # print("ERROR -- Invalid HTTP-Version token.")
            output.write(("ERROR -- Invalid HTTP-Version token." + "\n").encode('utf-8'))
        elif (checkSpurious(new)):
            # print("ERROR -- Spurious token before CRLF.")
            output.write(("ERROR -- Spurious token before CRLF." + "\n").encode('utf-8'))
        else:
            # print("Method = " + method)
            output.write(("Method = " + method + "\n").encode('utf-8'))
            # print("Request-URL = " + request_url)
            output.write(("Request-URL = " + request_url + "\n").encode('utf-8'))
            # print("HTTP-Version = " + HTTP_version)
            output.write(("HTTP-Version = " + HTTP_version + "\n").encode('utf-8'))
            output.write((passedFunctions(request_url, output)).encode('utf-8'))

        print(output.read())
        return output
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
    print("Connection Error", end="")
    sys.exit()

# Listen for at most 1 connection at a time
serverSocket.listen(1)

# Server should be up and running first,
# and listening to the incoming connections

while True:

    # sys.stdout = open('memory.txt', 'wt')
    output = tempfile.SpooledTemporaryFile(mode = 'w+b', max_size = 100000, encoding= None)
    output.write(("hellllo").encode("utf-8"))
    sys.stdout = sys.__stdout__
    print((output.read()).decode("utf-8"))
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
    output = main(message, output)

    # Send back to client
    # saved = open("memory.txt", "r")

    # sys.stdout = sys.__stdout__

    lines = output.readlines()
    print(lines)

    for x in lines:
        s.write(x.decode('utf-8'))
    s.flush()
    output.close()

    # Close the client connection socket
    connectionSocket.close()

serverSocket.close()
sys.exit()#Terminate the program after sending the corresponding data





