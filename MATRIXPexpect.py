# --*-- coding:utf-8 --*--
import os

import pexpect


# import time

def GMANEntrustPexpect(cmd, password):
    # 创建子应用
    child = pexpect.spawn(cmd)
    print(f"first output is :{child.before}")
    i = child.expect([pexpect.TIMEOUT, 'Passphrase:'])
    # 超时
    if i == 0:
        print("Timeout")
        return None
    # 准备输入密码
    if i == 1:
        # 输入密码
        print(f"output is :{child.before}")
        child.sendline(password)
        j = child.expect([pexpect.TIMEOUT, 'Repeat passphrase:'])
        # 超时
        if j == 0:
            print("Timeout")
            return None
        if j == 1:
            # print(f"output2 is :{child.before}")
            child.sendline(password)

            j = child.expect([pexpect.TIMEOUT, 'success'])
            # print(f"output3 is :{child.before}")
            print(f"output3 is :{child.after}")
            return child


if __name__ == '__main__':
    os.chdir("/Users/liqinghua/eric/test2/work")

    gmandir = f"{os.getcwd()}"
    chaindatadir = f"{os.getcwd()}{os.sep}chaindata"
    gman = f"{gmandir}{os.sep}gman"
    keyfile = f"{gmandir}{os.sep}key.json"
    entrustfile = f"{gmandir}{os.sep}entrust.json"
    password = "123456ABCDabcd@!"

    cmd = f"{gman} --datadir {chaindatadir} aes --aesin {keyfile} --aesout {entrustfile} "

    child = GMANEntrustPexpect(cmd, password)

    # time.sleep(1)
    if os.path.exists(entrustfile):
        print("Make sure generating entrust file successfully")
    else:
        print("Can not find the entrust file")
