###############################################################
#  This code by Ian Ferguson - 10.8.2019                      #
###############################################################

from socket import *
import sys
import string

###############################################################
#  Helper functions are implemented first.                    #
###############################################################


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
    opt = ''
    cnt = 0
    if inp.endswith((".htm", ".txt", ".html", ".HTM", ".TXT", ".HTML")):
        try:
            in_file = open(inp[1:], "r")
            text = in_file.readlines()
            for l in text:
                # print(l[:len(l)-1])
                opt += (l[:len(l)-1] + "\n")
                cnt += 1
        except FileNotFoundError:
            # print("404 Not Found: " + inp)
            opt += ("404 Not Found: " + inp + "\n")
            cnt += 1
        except IOError:
            # print(IOError)
            opt += IOError
            cnt += 1
    else:
        # print("501 Not Implemented: " + inp)
        opt += ("501 Not Implemented: " + inp + "\n")
        cnt += 1
    return opt, cnt

###############################################################
#  This is the main function from part one of                 #
#  the assignment.                                            #
###############################################################

def main(new):
    """
    The main function which loops through all lines of input,
    and splits the input into lists by whitespace. It then calls
    the functions to test the tokens in the input, and returns
    the results in one big string, called output.
    """
    output = ""
    cnt = 0

    stop = True
    while stop:
        new = ''.join(new)

        method = ""
        request_url = ""
        HTTP_version = ""

        output += new
        cnt += 1

        # if it is split by tabs:
        if new.find("\t") > 2:
            new = new.split("\t")

        # catching the case where there is a space at the beginning:
        if new[0] == " ":
            output += ("ERROR -- Invalid Method token." + "\n")
            cnt += 1
            return output, cnt

        # base space case split.
        new = new.split()
        try:
            method = new[0]
            request_url = new[1]
            HTTP_version = new[2]
        except Exception:
            pass

        if (len(new) == 0) or (not (checkGet(method))):
            output += ("ERROR -- Invalid Method token." + "\n")
            cnt += 1
        elif (len(new) == 1) or (not (checkURL(request_url))):
            output += ("ERROR -- Invalid Absolute-Path token." + "\n")
            cnt += 1
        elif (len(new) == 2) or (not (checkHTTP(HTTP_version))):
            output += ("ERROR -- Invalid HTTP-Version token." + "\n")
            cnt += 1
        elif checkSpurious(new):
            output += ("ERROR -- Spurious token before CRLF." + "\n")
            cnt += 1
        else:
            output += ("Method = " + method + "\n")
            cnt += 1
            output += ("Request-URL = " + request_url + "\n")
            cnt += 1
            output += ("HTTP-Version = " + HTTP_version + "\n")
            cnt += 1

            ote, count = passedFunctions(request_url)
            output += ote
            cnt += count
        return output, cnt


###############################################################
# This is the part of the code that acts as the server.       #
# It opens the socket, and will loop infinitely looking for   #
# new connections.  It reads each message, then generates     #
# the output for the message, and returns it.                 #
###############################################################


serverSocket = socket(AF_INET, SOCK_STREAM)

# Assign a port number from sys.argv
serverPort = int(sys.argv[1])

# Bind the socket to server address (default this machine)
# and server port, fail if OSError.
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
    # Wait for a new connection from the client
    # and accept it when requested
    # a new socket for data streams is returned from
    # the accept method
    connectionSocket, addr = serverSocket.accept()

    # Make a bidirectional stream (file-like) from socket
    # read and write operations can be used on the stream
    s = connectionSocket.makefile("rw")

    # Receives the request message from the client
    message = s.readline()

    # Calls the main function on the given message, and
    # takes its outputs.
    output, count = main(message)
    output = (str(count) + "\n" + output)

    # Send back to client
    sys.stdout = sys.__stdout__
    s.write(output)
    s.flush()

    # Close the client connection socket
    connectionSocket.close()

serverSocket.close()
sys.exit()




