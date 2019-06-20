import platform
import re
import subprocess
import sys


class MATRIXWebutil:
    Platform = "Windows"

    def __init__(self):
        self.checkplatform()

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
        #cmdlist=["open http://matrix.io"]
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


if __name__ == "__main__":
    print("It's MATRIX World!")
    url = "http://matrix.io"
    a=MATRIXWebutil()
    a.openurl(url)

    sys.exit()
