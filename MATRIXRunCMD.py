#!/usr/bin/python
# -*- coding: utf-8 -*-

import fcntl
import os
import time
from subprocess import Popen, PIPE


class Server(object):
    def __init__(self, args, server_env=None):
        if server_env:
            self.process = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE, env=server_env)
        else:
            self.process = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
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
                if e:
                    raise Exception('Error with process Reading!')
                else:
                    break
            elif r:
                return r.rstrip()
            else:
                time.sleep(max((x - time.time()) / tr, 0))
        return r.rstrip()


if __name__ == "__main__":
    cmd = "./gman --datadir ./chaindata --rpc --rpcaddr 0.0.0.0 --rpccorsdomain '*' --networkid 1 --debug --verbosity 5 --gcmode archive --outputinfo 1 --syncmode 'full'    "
    ServerArgs = ["./gman",
                  " --datadir ./chaindata --rpc --rpcaddr 0.0.0.0 --rpccorsdomain '*' --networkid 1 --debug --verbosity 5 --gcmode archive --outputinfo 1 --syncmode 'full'  "]

    workdir = "work"
    rootdir = os.getcwd()
    os.chdir(workdir)

    server = Server(ServerArgs)
    test_data = 'aa', 'vv', 'ccc', 'ss', 'ss', 'xx'
    for x in test_data:
        server.send(x)
        consoleoutput=server.recv()
        output = str(consoleoutput, 'utf-8')
        print(f"cmd execute result:\n{output}")

    os.chdir(rootdir)
