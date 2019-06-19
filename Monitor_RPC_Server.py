#!/usr/bin/en python
import os
from rpyc import Service
from rpyc.utils.server import ThreadedServer


class remote_call_script(Service):
    def exposed_iamshell(self):
        return os.system("./iamshell.sh")

    def exposed_iamperl(self):
        return os.system("./iamperl.pl")

    def exposed_iampython(self):
        return os.system("./iampython.py")


s = ThreadedServer(remote_call_script, port=11111, auto_register=False)
s.start()
