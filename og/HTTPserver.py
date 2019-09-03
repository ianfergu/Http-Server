import sys
import os.path
import string

stop = True
new = sys.stdin.read()

method = ""
request_url = ""
HTTP_version = ""

def checkGet(str):
    get = "GET"
    out = True
    for x in str:
        if x.isupper() == False:
            out = False
    for x in get:
        for y in str:
            if x.char != y.char:
                out = False
    return out

def checkURL(str):
    out = True
    if str[0] != "/":
        out = False
    if str[len(str)-1] == "/":
        out = False
    if os.path.isfile(str) == False:
        out = False
    charsAllowed=(string.ascii_lowercase + string.ascii_uppercase + string.digits + "." + "_" + "/")
    for x in str():
        if x not in charsAllowed:
            out = False
    return out

def checkHTTP(str):
    out = True
    #“HTTP” “/” +DIGIT “.” +DIGIT
    if str[0:3] != "HTTP":
        out = False
    if str[4] != "/":
        out = False
    if str[5] not in string.digits:
        out = False
    if str[6] != ".":
        out = False
    if str[7] not in string.digits:
        out = False
    #potential for errors v
    if str.find("\n") == -1:
        out = False
    return out

while stop != False:
    print(new)
    #tab case
    if new.find("\t") > 2:
        new = new.split("\t")
    #base space case
    new = new.split(" ")
    try:
        method = new[0]
        request_url = new[1]
        HTTP_version = new[2]
    except Exception:
        print("Error")

    if (checkGet(method)) == False:
        print("ERROR -- Invalid Method token.")

    if (checkURL(request_url)) == False:
        print("ERROR -- Invalid Absolute-Path token.")

    if (checkHTTP(HTTP_version)) == False:
        print("ERROR -- Invalid HTTP-Version token.")











