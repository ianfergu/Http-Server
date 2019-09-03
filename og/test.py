import sys
import os.path
import string
import time

stop = True
#new = sys.stdin.read()

def checkGet(inp):
    get = "GET"
    out = True
    for x in inp:
        if x.isupper() == False:
            out = False
    for x in range(len(get)-1):
        if ord(inp[x]) != ord(get[x]):
            out = False
    return out

def checkURL(inp):
    out = True
    if inp[0] != "/":
        out = False
#    if os.path.isfile(inp) == False:
#        out = False
    charsAllowed=(string.ascii_lowercase + string.ascii_uppercase + string.digits + "." + "_" + "/")
    for z in inp:
        if z not in charsAllowed:
            out = False
    return out

def checkHTTP(inp):
    try:
        out = True
        #“HTTP” “/” +DIGIT “.” +DIGIT
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
        #potential for errors v
        #if inp.find("\n") == -1:
         #   out = False
        return out
    except Exception:
        out= False
    return out

def main():
    method = ""
    request_url = ""
    HTTP_version = ""
    stop = True
    zen = open("texts.txt", "r")
    new = zen.readline()
    while new != "":

        #new = input("enter command")
        print(new, end = "")
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
        elif (checkURL(request_url)) == False:
            print("ERROR -- Invalid Absolute-Path token.")
        elif (checkHTTP(HTTP_version)) == False:
            print("ERROR -- Invalid HTTP-Version token.")
        #time.sleep(5)
        new = zen.readline()
    zen.close()

main()






