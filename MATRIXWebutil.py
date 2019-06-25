import os
import platform
import re
import stat
import subprocess
import sys


class MATRIXWebutil:
    Platform = "Windows"

    def __init__(self):
        self.Platform = "Windows"
        self.checkplatform()
        self.childProcess = subprocess.Popen("echo Hello MATRIX Subprocess!", stdin=subprocess.PIPE,
                                          stdout=subprocess.PIPE,
                                          stderr=subprocess.PIPE,
                                          shell=True)

    def openurl(self, url):
        print(f"Openning {url}....")
        if self.Platform == "Windows":
            self.openurl_win(url)
        elif self.Platform == "Linux":
            self.openurl_linux(url)
        elif self.Platform == "Darwin":
            self.openurl_mac(url)
        else:
            self.openurl_mac(url)

    def exec(self, cmd, arg=""):
        cmdlist = f"{cmd} {arg}"
        # cmdlist=["open http://matrix.io"]
        print(f"exec {cmdlist}")
        subprocess.call(cmdlist, shell=True)

    def openurl_mac(self, url):
        if not self.urlvalid(url):
            return False

        cmd = "open"
        arg = url

        self.exec(cmd, arg)
        return True

    def openurl_win(self, url):
        if not self.urlvalid(url):
            return False

        cmd = "start"
        arg = url

        self.exec(cmd, arg)
        return True

    def openurl_linux(self, url):
        if not self.urlvalid(url):
            return False

        cmd = "firefox"
        arg = url

        self.exec(cmd, arg)
        return True

    def urlvalid(self, url):
        pattern = '((http|ftp|https)://)(([a-zA-Z0-9\._-]+\.[a-zA-Z]{2,6})|([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}))(:[0-9]{1,4})*(/[a-zA-Z0-9\&%_\./-~-]*)?'
        # pattern = '(https?://[^\s)";]+(\.(\w|/)*))'
        links = re.compile(pattern).findall(url)

        if links == "":
            print("Please input valid link URL")
            return False
        else:
            return True

    def checkplatform(self):
        sysstr = platform.system()
        if (sysstr == "Windows"):
            print("Now We will do Windows tasks")
            self.Platform = "Windows"
        elif (sysstr == "Linux"):
            print("Now We will do Linux tasks")
            self.Platform = "Linux"
        elif (sysstr == "Darwin"):
            print("Now We will do MacOS tasks")
            self.Platform = "Darwin"
        else:
            self.Platform = "Windows"
            print("Other System tasks")

    # def runwincmd(self,cmd):
    def SaveExeclinux(self, cmd, filename="a.cmd"):

        with open(filename, 'w') as f:
            f.write(cmd)
        os.chmod(filename, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
        localargs = f"xterm -e {cmd} &"

        self.childProcess = subprocess.Popen(localargs, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                          stderr=subprocess.PIPE,
                                          shell=True)
        return self.childProcess

    def SaveExecWin(self, cmd, filename="a.bat"):

        with open(filename, 'w') as f:
            f.write(cmd)

        os.chmod(filename, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
        localargs = f"start {filename}"  # f"xterm -e {cmd} &"

        # note we should not use Popen mathod since it will block the program"
        # self.childProcess = subprocess.call(localargs, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
        #                                   stderr=subprocess.PIPE,
        #                                   shell=True)

        self.childProcess = subprocess.call(localargs,shell=True)
        #i = 0

        # while self.childProcess.poll() is None and (i < 100):
        #     line = self.childProcess.stdout.readline()
        #     line = line.strip()
        #
        #     lineok = str(line, 'utf-8')
        #     print(lineok)
        #     i = i + 1
        #
        return self.childProcess

    def saveExec(self, cmd, filename="a.cmd"):
        print(f"start {cmd}....")
        if self.Platform == "Windows":
            return self.SaveExecWin(cmd, filename)
        elif self.Platform == "Linux":
            return self.SaveExeclinux(cmd, filename)
        elif self.Platform == "Darwin":
            return self.SaveExeclinux(cmd, filename)
        else:
            return self.SaveExecWin(cmd, filename)


if __name__ == "__main__":
    print("It's MATRIX World!")
    url = "http://matrix.io"
    a = MATRIXWebutil()
    a.openurl(url)

    workdir = "../test3/work"
    rootdir = os.getcwd()
    os.chdir(workdir)
    gmandir = f"{os.getcwd()}"
    chaindatadir = f"{os.getcwd()}{os.sep}chaindata"
    if a.Platform == "Windows":
        postfix = ".exe"
    else:
        postfix = ""

    ServerArgs = f"{gmandir}{os.sep}gman{postfix} --datadir {chaindatadir} --rpc --rpcaddr 0.0.0.0 --rpccorsdomain '*' --networkid 1 --debug --verbosity 5 --gcmode archive --outputinfo 0 --syncmode full  "

    print(ServerArgs)
    a.saveExec(ServerArgs)

    sys.exit()
