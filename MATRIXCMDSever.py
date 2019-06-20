#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import subprocess
import time
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
# code:utf-8
from PyQt5.QtWidgets import *

class MATRIXCMDServer(object):
    def __init__(self, args):
        c = ''
        cmd = c.join(args)
        # cmd = args
        print("Execute cmd:")
        print(cmd)

        self.childprocess = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                             shell=True)
        print("Program start")
        # for i in range(100):
        #     info=self.childprocess.stdout.readline()
        #     output = str(info, 'utf-8')
        #     print(output)

    def readcmdResult(self, linenum=100):

        if linenum < 1:
            linenum = 1
        result = ''
        for i in range(linenum):
            if self.childprocess.poll() is None:
                line = self.childprocess.stdout.readline()
                line = line.strip()
                lineok = str(line, 'utf-8')
                if lineok:
                    #print('Subprogram output: [{}]'.format(lineok))
                    result = f"result{lineok}"
                return result

        if self.childprocess.returncode == 0:
            print('\n\nSubprogram success\n\n')
        else:
            print('\n\nSubprogram failed\n\n')

if __name__ == "__main__":

    workdir = "../test3/work"
    rootdir = os.getcwd()
    os.chdir(workdir)
    gmandir = f"{os.getcwd()}"
    chaindatadir = f"{os.getcwd()}{os.sep}chaindata"

    ServerArgs = [f"{gmandir}{os.sep}gman",
                  f" --datadir {chaindatadir} --rpc --rpcaddr 0.0.0.0 --rpccorsdomain '*' --networkid 1 --debug --verbosity 3 --gcmode archive --outputinfo 1 --syncmode full  "]

    server = MATRIXCMDServer(ServerArgs)
    while server.childprocess.poll() is None:
        text=server.readcmdResult()
        print(text)

    os.chdir(rootdir)
