#!/usr/bin/env python
# coding:utf-8
import subprocess
import shlex
import os, stat
#import win32api

def SaveExeclinux(cmd,filename="a.cmd"):

    with open(filename, 'w') as f:
        f.write(cmd)
    os.chmod(filename, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
    localargs=f"xterm -e {cmd} &"

    myProcess = subprocess.call(localargs, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                 shell=True)
    return myProcess

def SaveExecWin(cmd,filename="a.cmd"):

    with open(filename, 'w') as f:
        f.write(cmd)
    os.chmod(filename, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
    localargs=f"cmd.exe /c {filename}" #f"xterm -e {cmd} &"

    p = subprocess.Popen(localargs, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    i=0
    curline = p.stdout.readline()
    while (curline != b'' and i < 100):
        print(curline)
        curline = p.stdout.readline()
        i=i+1

    myProcess = subprocess.call(localargs, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                 shell=True)
    return myProcess



if __name__ == "__main__":
    execcmd="ls -l"
    cmd=f"/Applications/Utilities/Terminal.app/Contents/MacOS/Terminal -e '{execcmd}' & "

    #localargs = shlex.split(cmd)
    #myProcess = subprocess.Popen(localargs, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)

    workdir = "../test3/work"
    rootdir = os.getcwd()
    os.chdir(workdir)
    gmandir = f"{os.getcwd()}"
    chaindatadir = f"{os.getcwd()}{os.sep}chaindata"

    ServerArgs = f"{gmandir}{os.sep}gman --datadir {chaindatadir} --rpc --rpcaddr 0.0.0.0 --rpccorsdomain '*' --networkid 1 --debug --verbosity 5 --gcmode archive --outputinfo 0 --syncmode full  "

    print(ServerArgs)
    saveExec(ServerArgs)

