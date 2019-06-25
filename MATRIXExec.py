#!/usr/bin/python
# -*- coding: utf-8 -*-

import fcntl
import os
import time
from subprocess import Popen, PIPE
import shlex

class MATRIXExec(object):
    def __init__(self, args, server_env=None):
        localargs=shlex.split(args)
        print("Execute cmd:")
        print(localargs)
        if server_env:
            self.process = Popen(localargs, stdin=PIPE, stdout=PIPE, stderr=PIPE, env=server_env)
        else:
            self.process = Popen(localargs, stdin=PIPE, stdout=PIPE, stderr=PIPE)
            print(f"Popen({args}, stdin=PIPE, stdout=PIPE, stderr=PIPE)")
        flags = fcntl.fcntl(self.process.stdout, fcntl.F_GETFL)
        fcntl.fcntl(self.process.stdout, fcntl.F_SETFL, flags | os.O_NONBLOCK)




if __name__ == "__main__":
    workdir = "../test3/work"
    rootdir = os.getcwd()
    os.chdir(workdir)
    gmandir = f"{os.getcwd()}"
    chaindatadir = f"{os.getcwd()}{os.sep}chaindata"

    ServerArgs = f"{gmandir}{os.sep}gman --datadir {chaindatadir} --rpc --rpcaddr 0.0.0.0 --rpccorsdomain '*' --networkid 1 --debug --verbosity 5 --gcmode archive --outputinfo 0 --syncmode full  "

    server = MATRIXExec(ServerArgs)
    test_data = 'aa', 'vv', 'ccc', 'ss', 'ss', 'xx'
    for x in test_data:
        server.send(x)
        consoleoutput = server.recv()
        if not consoleoutput=="":
            output = str(consoleoutput, 'utf-8')
            print(f"cmd execute result:\n{output}")

    os.chdir(rootdir)
