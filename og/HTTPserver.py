import sys
import string


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
            for lines in text:
                print(lines[:len(lines)-1])
        except FileNotFoundError:
            print("404 Not Found: " + inp)
        except IOError:
            print(IOError)
    else:
        print("501 Not Implemented: " + inp)


def main():
    """
    The main function which loops through all lines of input,
    and splits the input into lists by whitespace. It then calls
    the functions to test the tokens in the input, and prints the
    results.
    """
    zen = sys.stdin.readlines()
    for new in zen:
        method = ""
        request_url = ""
        HTTP_version = ""
        print(new, end = "")
        #tab case
        if new.find("\t") > 2:
            new = new.split("\t")
        #base space case
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


main()
