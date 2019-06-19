# !/usr/bin/python
# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""
import os
import platform
import re
import rpyc
import subprocess
import sys
import threading  # 引入线程
from typing import List, Any

from MATRIXDownloadURL import *


# from rpyc import Service
# from rpyc.utils.server import ThreadedServer
# from time import sleep

class MATRIXCmd():
    #gmanBaseURL = 'localhost'
    gmanBaseURL = "https://matrix.io/Download/"
    Platform = ""
    updateversion = 0
    localGmanName = "gman"
    GmanURL = ""
    localpath = "~/gman"
    needUpdateGman = 0
    localversion = -1
    #host = "api85.matrix.io"
    host = 'localhost'
    port = 9999

    def __init__(self):
        self.Platform = self.checkplatform()
        self.GmanURL = self.checkDownloadPath()

    def mkdirGman(self, rootdir):
        print(f"Gman will be located in {rootdir}")
        self.mkdir(rootdir)
        self.mkdir(f"{rootdir}\\chaindata")
        self.mkdir(f"{rootdir}\\src")

    def mkdir(path):
        # 去除首位空格
        path = path.strip()
        # 去除尾部 \ 符号
        path = path.rstrip("\\")

        # 判断路径是否存在
        # 存在     True
        # 不存在   False
        isExists = os.path.exists(path)

        # 判断结果
        if not isExists:
            # 如果不存在则创建目录
            # 创建目录操作函数
            os.makedirs(path)
            print(f"{path}创建成功")
            return True
        else:
            # 如果目录存在则不创建，并提示目录已存在
            print(f"{path}目录已存在")
            return False

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

    def execute_cmd(cmd):
        p = subprocess.Popen(cmd,
                             shell=True,
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()
        if p.returncode != 0:
            return p.returncode, stderr
        return p.returncode, stdout

        # cmd = 'ls /u01'
        # returncode, out = execute_cmd(cmd)
        #
        # if returncode != 0:
        #     raise SystemExit('execute {0} err :{1}'.format(cmd, out))
        # else:
        #     print("execute command ({0} sucessful)".format(cmd))

    def checkDownloadPath(self):
        self.checkplatform()
        self.getGmanName()
        self.MATRIXVersionRPC(self.host, self.port)
        # gmanBaseURL = "https://matrix.io/Download/"
        # Platform = ""
        # updateversion = 0
        # localGmanName = "gman"

        self.GmanURL = f"{self.gmanBaseURL}/{self.Platform}/{self.updateversion}/{self.localGmanName}.zip"
        print(f"Downloading Files from URL:{self.GmanURL}")

    def downloadGman(self):
        self.checkDownloadPath()
        # url = "https://www.matrix.io/uploads/file/gman(mac).zip"
        download_from_url(self.GmanURL, "./gman.zip")

    def isGmanUpdate(self):
        self.checkplatform()
        self.getGmanName()
        self.checklocalversion()
        self.MATRIXVersionRPC(self.host, self.port)
        if self.localversion != self.updateversion:
            self.needUpdateGman = 1
        else:
            self.needUpdateGman = 0

    def getGmanName(self):
        self.checkplatform()
        if self.Platform == "Windows":
            self.localGmanName = "gman.exe"
        elif self.Platform == "Linux":
            self.localGmanName = "gman"
        elif self.Platform == "Darwin":
            self.localGmanName = "gman"
        else:
            self.localGmanName = "gman.exe"

    def checklocalversion(self):
        print("check version and platform!")
        cmd = f"{self.localpath}/{self.localGmanName} --version"
        returncode, out = self.execute_cmd(cmd)

        if returncode != 0:
            print('execute {0} err :{1}'.format(cmd, out))
            self.localversion = -1
        else:
            print("execute command ({0} sucessful)".format(cmd))
            self.localversion = out

    def MATRIXVersionRPC(self, host, port):
        # 参数主要是host, port

        try:

            conn = rpyc.connect(host, port)
            # 调用服务器端的方法，格式为：conn.root.xxx。xxx代表服务器端的方法名
            # get_time是服务端的那个以"exposed_"开头的方法
            result = conn.root.testVersion()
            print(f"MATRIX Version is {result} ")
            # test是服务端的那个以"exposed_"开头的方法
            self.updateversion = result
            conn.close()

        except (ConnectionError, TimeoutError) as e:
            # conn.disconnect()

            print("Check MATRIX GMAN Service Connection!No Server with RPC....\n\n")
        else:
            print("RPC connect OK! Do more job with RPC server!")

    def _execute(self, connection, command, *args):
        try:
            return command(*args)
        except (ConnectionError, TimeoutError) as e:
            connection.disconnect()
            if not (connection.retry_on_timeout and
                    isinstance(e, TimeoutError)):
                raise
            # Connect manually here. If the Redis server is down, this will
            # fail and raise a ConnectionError as desired.
            connection.connect()
            # the ``on_connect`` callback should haven been called by the
            # connection to resubscribe us to any channels and patterns we were
            # previously listening to
            return command(*args)

    def checkAddressValid(address):
        inputstr = address.strip()
        # regPattern = 'r\'^MAN\.[a-km-zA-HJ-NP-Z1-9]{25,34}\''
        # regPattern= '''r'^MAN\.[a-km-zA-HJ-NP-Z1-9]{25,34}\''''
        # regPattern=r'^https?:/{2}\w.+$'
        # pattern = re.compile(regPattern) #This method is not ok!
        pattern = re.compile(r'^MAN\.[a-km-zA-HJ-NP-Z1-9]{25,34}')

        # 使用Pattern匹配文本，获得匹配结果，无法匹配时将返回None
        match = pattern.match(inputstr)
        if match:
            valid_address = inputstr
        else:
            valid_address = []

        return match, valid_address


# class TestService(Service):
#     # 对于服务端来说， 只有以"exposed_"打头的方法才能被客户端调用，所以要提供给客户端的方法都得加"exposed_"
#     def exposed_testVersion(self):
#         return 5


if __name__ == "__main__":
    print("It's MATRIX World!")
    man1 = MATRIXCmd()
    man1.MATRIXVersionRPC(man1.host, man1.port)
    print("Client Working!")
    t2 = threading.Thread(target=man1.MATRIXVersionRPC(man1.host, man1.port))
    sys.exit()
