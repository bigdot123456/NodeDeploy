#!/usr/bin/python
# -*- coding: utf-8 -*-

import fcntl
import os
import time
from subprocess import Popen, PIPE
import shlex

class Server(object):
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

    def send(self, data):
        subcmd = bytes(data + "\n", encoding="utf8")
        self.process.stdin.write(subcmd)

    #        self.process.stdin.flush()

    def recv(self, t=.1, e=1, tr=5, stderr=0):
        time.sleep(t)
        if tr < 1:
            tr = 1
        x = time.time() + t
        r = ''
        pr = self.process.stdout
        if stderr:
            pr = self.process.stdout
        while time.time() < x or r:
            r = pr.read()
            if r is None:
                return ""
            elif r:
                return r.rstrip()
            else:
                time.sleep(max((x - time.time()) / tr, 0))
        return r.rstrip()


if __name__ == "__main__":
    workdir = "../test3/work"
    rootdir = os.getcwd()
    os.chdir(workdir)
    gmandir = f"{os.getcwd()}"
    chaindatadir = f"{os.getcwd()}{os.sep}chaindata"

    ServerArgs = f"{gmandir}{os.sep}gman --datadir {chaindatadir} --rpc --rpcaddr 0.0.0.0 --rpccorsdomain '*' --networkid 1 --debug --verbosity 5 --gcmode archive --outputinfo 0 --syncmode full  "

    server = Server(ServerArgs)
    test_data = 'aa', 'vv', 'ccc', 'ss', 'ss', 'xx'
    for x in test_data:
        server.send(x)
        consoleoutput = server.recv()
        if not consoleoutput=="":
            output = str(consoleoutput, 'utf-8')
            print(f"cmd execute result:\n{output}")

    os.chdir(rootdir)
