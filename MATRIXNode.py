# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""

import json

import fire
from PyQt5 import QtCore

from MATRIXCMDSever import *
from MATRIXCmd import *
from MATRIXGetURLContent import *
from MATRIXPassword import *
from MATRIXStringTools import *
# from MATRIXRunCMD import *
from MATRIXWebutil import *
# from PyQt5.QtWidgets import QMainWindow
# from PyQt5.QtCore import pyqtSlot
from Ui_MATRIXNode import Ui_MainWindow
from MATRIXPexpect import *
from NodeConfig import *

class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    vdepositValue = 0
    mdepositValue = 0
    transferValue = 0
    listlimited = 8192

    a0_Address = ""
    a1_Address = ""
    transfer_Address = ""
    superNode_Address = ""

    fixedPeriod = "活期"
    select_VM = "Miner"
    select_actor = "SuperNode"
    NodeRootDir = f".{os.sep}"
    MainFile = "gman"
    browser = ""

    url = 'https://www.matrix.io/downloads/'

    cmdNum = 0
    NodeServer = ""
    cmdResult = ""

    networkID=1
    verbosityLevel = 3
    output2File = 0
    rpcaddr = "0.0.0.0"
    syncmode = "full"
    gcmode = "archive"

    entrustPass=""

    # self.ValidatorradioButton
    # self.FollowSuperNode
    # self.CreateSuperNode
    # self.NormalNode
    # self.MinerradioButton

    # self.Fixed3MradioButton
    # self.Fixed6MradioButton
    # self.CurrentradioButton
    # self.Fixed1MradioButton
    # self.Fixed12Mradiobutton

    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)
        self.setFixedSize(self.width(), self.height())
        print("Start MATRIX World!")

        self.bg1 = QButtonGroup(self)
        self.bg1.addButton(self.NormalNode, 11)
        self.bg1.addButton(self.CreateSuperNode, 12)
        self.bg1.addButton(self.FollowSuperNode, 13)

        self.bg2 = QButtonGroup(self)
        self.bg2.addButton(self.MinerradioButton, 21)
        self.bg2.addButton(self.ValidatorradioButton, 22)

        self.bg3 = QButtonGroup(self)
        self.bg3.addButton(self.CurrentradioButton, 31)
        self.bg3.addButton(self.Fixed1MradioButton, 32)
        self.bg3.addButton(self.Fixed3MradioButton, 33)
        self.bg3.addButton(self.Fixed6MradioButton, 34)
        self.bg3.addButton(self.Fixed12Mradiobutton, 35)

        self.NodeBootLogText.document().setMaximumBlockCount(1000)
        self.NodeServiceText.document().setMaximumBlockCount(1000)

        self.browser = MATRIXWebutil()
        self.DownloadThread = DownloadThread()

        self.NodeRootDir = os.getcwd()
        self.DefaultWorkDirLabel.setText(self.NodeRootDir)
        self.show()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, '确认', '确认退出MATRIX节点部署环境吗', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    @pyqtSlot()
    def on_WalletAddress_editingFinished(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        # raise NotImplementedError
        address = self.WalletAddress.text()
        match, valid_address = MATRIXCmd.checkAddressValid(address)

        if match:
            # 使用Match获得分组信息
            print("Wallet A0 account Ok.")
            self.WalletAddressLabel.setText('钱包A0账户正常')
            self.a0_Address = valid_address
            depoly_msg = '提供的钱包账户：' + valid_address
            print(f"{depoly_msg}")
        else:
            self.WalletAddressLabel.setText('钱包A0账户不正常，格式为MAN.XXXXX')
            print("Wallet a0 account Error.")

            self.WalletAddress.clear()
            # self.WalletAddress.setFocus()
            return

    @pyqtSlot()
    def on_WorkAccount_editingFinished(self):
        """
        Slot documentation goes here.
        这是智能合约账户
        """
        # TODO: not implemented yet
        address = self.WorkAccount.text()
        match, valid_address = MATRIXCmd.checkAddressValid(address)

        if match:
            # 使用Match获得分组信息
            print("Attention other SuperNode account Ok.")
            self.WalletAddressLabel.setText('参加其它超级节点的目标账户正常，检查该账户的智能合约')
            self.superNode_Address = valid_address
            depoly_msg = '参加的超级节点账户为：' + valid_address
            print(f"{depoly_msg}")
        else:
            self.WalletAddressLabel.setText('参加其它超级节点的目标账户不正常，格式为MAN.XXXXX')
            print("SuperNode SmartContract account Error.")

            self.WorkAccount.clear()
            # self.WorkAccount.setFocus()
            return

    @pyqtSlot()
    def on_entrustAccount_editingFinished(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        # raise NotImplementedError
        # raise NotImplementedError
        address = self.entrustAccount.text()
        match, valid_address = MATRIXCmd.checkAddressValid(address)

        if match:
            # 使用Match获得分组信息
            print("entrust A1 account Ok.")
            self.WalletAddressLabel.setText('A1账户正常')
            self.a1_Address = valid_address
            depoly_msg = '抵押的账户为：' + valid_address
            print(f"{depoly_msg}")
        else:
            self.WalletAddressLabel.setText('抵押A1账户不正常，格式为MAN.XXXXX')
            print("entrust a1 account Error.")

            self.entrustAccount.clear()
            # self.entrustAccount.setFocus()
            return

    @pyqtSlot()
    def on_TransferWalletAddress_editingFinished(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        # raise NotImplementedError
        address = self.TransferWalletAddress.text()
        match, valid_address = MATRIXCmd.checkAddressValid(address)

        if match:
            # 使用Match获得分组信息
            print("transfer account Ok,please manually check this people are your friends.")
            self.WalletAddressLabel.setText('转账对象的账户正常')
            self.transfer_Address = valid_address
            depoly_msg = '转账目标账户为：' + valid_address
            print(f"{depoly_msg}")
        else:
            self.WalletAddressLabel.setText('转账对象的账户不正常，格式为MAN.XXXXX')
            print("transfer account Error.")

            self.TransferWalletAddress.clear()
            # self.entrustAccount.setFocus()
            return

    @pyqtSlot()
    def on_VDepositValue_editingFinished(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        # raise NotImplementedError
        value = self.VDepositValue.text()
        if JudgeStr2Float(value):
            self.depositValue = float(value)
            print(f"Validator Deposit with {value} MAN")
        else:
            self.vdepositValue = 0
            self.VDepositValue.clear()
            # self.VDepositValue.setFocus()

    @pyqtSlot()
    def on_MDepositValue_editingFinished(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        # raise NotImplementedError
        value = self.MDepositValue.text()
        if JudgeStr2Float(value):
            self.mdepositValue = float(value)
            print(f"Validator Deposit with {value} MAN")
        else:
            self.mdepositValue = 0
            self.MDepositValue.clear()
            # self.MDepositValue.setFocus()

    @pyqtSlot()
    def on_TransferValue_editingFinished(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        # raise NotImplementedError
        transferValueStr = self.TransferValue.text()
        if JudgeStr2Float(transferValueStr):
            self.transferValue = float(transferValueStr)
            print(f"You will transfer {self.transferValue}")
            self.WalletAddressLabel.setText(f'转账金额为{transferValueStr}')
        else:
            self.WalletAddressLabel.setText(f'输入正确的转账金额，当前输入为：{transferValueStr}')
            print(f"You should input correct value! {self.transferValue} is illegal value")
            self.TransferValue.clear()

    @pyqtSlot()
    def on_Current2Fixed_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError

    @pyqtSlot()
    def on_ValidatorradioButton_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        # raise NotImplementedError
        print("Select Validator.")
        self.select_VM = "Validator"
        self.mdepositValue = 0
        self.MDepositValue.clear()
        self.VDepositValue.setFocus()

    @pyqtSlot()
    def on_MinerradioButton_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        # raise NotImplementedError
        print("Select Miner.")
        self.select_VM = "Miner"
        self.vdepositValue = 0
        self.VDepositValue.clear()
        self.MDepositValue.setFocus()

    @pyqtSlot()
    def on_Fixed3MradioButton_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        # raise NotImplementedError
        print("Select 3 Month cash fixed deposit.")
        self.select_actor = "Month3"

    @pyqtSlot()
    def on_Fixed6MradioButton_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        # raise NotImplementedError

        print("Select 6 Month cash fixed deposit.")
        self.select_actor = "Month6"

    @pyqtSlot()
    def on_CurrentradioButton_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        # raise NotImplementedError
        print("Select current cash deposit. If you select it, cash will be released after 7 days")
        self.select_actor = "Month0"

    @pyqtSlot()
    def on_Fixed1MradioButton_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        # raise NotImplementedError
        print("Select 6 Month cash fixed deposit. If you select it, cash will be released after 6 month")
        self.select_actor = "Month1"

    @pyqtSlot()
    def on_Fixed12Mradiobutton_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        # raise NotImplementedError
        print("Select 6 Month cash fixed deposit. If you select it, cash will be released after 6 month")
        self.select_actor = "Month12"

    @pyqtSlot()
    def on_CreateSuperNode_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        # raise NotImplementedError
        print("Select beccome SuperNode Node,call others attend in! Best Wish")
        self.select_actor = "SuperNode"

    @pyqtSlot()
    def on_FollowSuperNode_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        # raise NotImplementedError
        print("Select following Other SuperNode. Best Wish")
        self.select_actor = "FollowSuperNode"

    @pyqtSlot()
    def on_NormalNode_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        # raise NotImplementedError
        print("Select Normal Node,not need others attend in! Best Wish")
        self.select_actor = "NormalNode"

    @pyqtSlot()
    def on_Deposit_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError

    @pyqtSlot()
    def on_DecreaseDeposit_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError

    # @pyqtSlot(int, int)
    # def on_MDepositValue_cursorPositionChanged(self, p0, p1):
    #     """
    #     Slot documentation goes here.
    #
    #     @param p0 DESCRIPTION
    #     @type int
    #     @param p1 DESCRIPTION
    #     @type int
    #     """
    #     # TODO: not implemented yet
    #     raise NotImplementedError

    @pyqtSlot()
    def on_GenerateA1_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        # raise NotImplementedError
        self.on_GenerateRandomAccountAddress_clicked()

    @pyqtSlot()
    def on_CloseWallet_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError

    @pyqtSlot()
    def on_ConfirmWalletOP_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError

    @pyqtSlot()
    def on_OpenWallet_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError

    @pyqtSlot()
    def on_AutoCloseWallet_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError

    def checkGMAN(self):

        os.chdir(self.NodeRootDir)
        workdir = f".{os.sep}work"

        try:
            os.chdir(workdir)
        except:

            result = "Error in change directory! You should change to correct Path which contain gman"
            print(result)
            self.cmdResult = result
            self.OnlyDisplay("Account A1 Generation", result)
            os.chdir(self.NodeRootDir)
            return False

        try:
            f = open(self.browser.gmanName)
            f.close()

        except IOError:
            result = "Error in open GMAN! You should change to correct Path which contain gman"
            print(result)
            self.cmdResult = result
            self.OnlyDisplay("Account A1 Generation", result)
            QMessageBox.warning(self,"GMAN Doesn't exist in current directory! Please Change directory or download it!","GMAN Doesn't exist in current directory! Please Change current directory or download it!\n主程序gman不存在当前目录的work目录下，无法继续执行，请注意！")
            os.chdir(self.NodeRootDir)
            return False

        return True

    def grepMANAddress(self,line):
        manflag="MAN"
        if manflag in line:
            matchObj = re.split(r'(")(MAN\.[a-km-zA-HJ-NP-Z1-9]{2,34})(")', line)
            # r'(")(MAN\.[a-km-zA-HJ-NP-Z1-9]{2,34})(")'

            if matchObj:
                for i in matchObj:
                    if manflag in i:
                        self.a1_Address = i
                        print(f"成功生成账户{self.a1_Address}")  # self.a1_Address =matchObj[2]
                        return True
                # matchObj.group()
        else:
            print(f"检查是否启动GMAN节点，结果为!{line}")
            #QMessageBox.warning(self, "警告", f"检查是否启动GMAN节点，输出日志为：{line}")

        return False

    @pyqtSlot()
    def on_GenerateRandomAccountAddress_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        # raise NotImplementedError
        print("Generate a random Account for deposit! You should input password for this account!")

        if not self.checkGMAN():
            #os.chdir(self.NodeRootDir)
            return False

        pwd = MATRIXPasswordDiaglog()  # DIY密码输入框
        r = pwd.exec_()  # 执行密码输入框
        if not r:
            print("You discard generating password and can't generate a random account!")
            return
        else:
            passwordOK = pwd.text
            print(f"password is {passwordOK}")

        ipcname = f".{os.sep}chaindata{os.sep}gman.ipc"
        gman = f".{os.sep}{self.browser.gmanName}"

        # cmd=f"echo \"personal.newAccount(\\\"{passwordOK}\\\")\" | {gman} attach {ipcname} | grep 'MAN.' "
        cmd = f"echo \"personal.newAccount(\\\"{passwordOK}\\\")\" | {gman} attach {ipcname} "

        line = self.executeAndDisplay(cmd)

        if self.grepMANAddress(line):
            print(f"Succussful generating A1 Address: {self.a1_Address}")

        else:
            QMessageBox.warning(self, "警告", f"检查是否启动GMAN节点，输出日志为：{line}")
            return False

        self.entrustAccount.setText(self.a1_Address)
        self.WalletAddressLabel.setText(f"设定委托账户为当前随机账户{self.a1_Address}，请保管好账户密码")
        demo_json = """
        [
                {
                    "Address":"MAN.427Suh4uPVqdBzrSbn2u6FrNz9rYj",
                    "Password":"testPassword"
                },
                {
                    "Address":"MAN.7nk8CuT9ZCBfSfYpfiXaomHvk4Nn",
                    "Password":"xxx"
                },
                {
                    "Address":"MAN.49nECVaeeHYQ2H8t91r33yrfCMhXA",
                    "Password":"xxx"
                },
                {
                    "Address":"MAN.2SaM3sU8K6bAEG4eA15g6ZtwA5UuZ",
                    "Password":"xxx"
                },
                {
                    "Address":"MAN.4GoTEXV33PEaRrHL1rA46UtZsDtaz",
                    "Password":"xxx"
                },
                {
                    "Address":"MAN.3keXfyBY2HRkRNYvhaynkGD6ezmNh",
                    "Password":"xxx"
                }
            ]
        """
        # save result to json file
        json_dict = {
            'Address': self.a1_Address,
            'Password': passwordOK
        }

        # 写入 JSON 数据
        with open('key.json', 'w') as f:
            f.write("[\n")
            json.dump(json_dict, f)
            f.write("\n]")

        # 读取数据
        with open('key.json', 'r') as f:
            data_check = json.load(f)

        os.chdir(self.NodeRootDir)

    @pyqtSlot()
    def on_NodeInit_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        # raise NotImplementedError
        # rootdir = self.DefaultWorkDirLabel.text() #os.getcwd()

        if not self.checkGMAN():
            #os.chdir(self.NodeRootDir)
            return False

        gman = f".{os.sep}{self.browser.gmanName}"

        cmd = f"{gman} --datadir ./chaindata  init MANGenesis.json"

        print(f"Init Gman with command:\ncd work;\n{gman} --datadir ./chaindata  init MANGenesis.json \n\n")
        self.executeAndDisplay(cmd)
        # child1 = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        # outs, errs = child1.communicate()
        #
        # # output=str(outs).decode('string_escape')
        # output = str(outs, 'utf-8')
        # print(f"cmd execute result:\n{output}")
        #
        # self.cmdLogText.setPlainText(cmd)
        # self.listWidget.addItem(cmd)
        # self.NodeBootLogText.append(output)
        QMessageBox.about(self, "MATRIX初始化节点状态", f"执行命令为：{cmd},执行结果为\n{self.cmdResult}")

        os.chdir(self.NodeRootDir)

    @pyqtSlot()
    def on_SignatureInputCMD_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        # raise NotImplementedError
        text = self.LineEditInput.text()
        print(f"signature the input text:{text}!")

    @pyqtSlot()
    def on_SetDefaultWorkDir_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        # raise NotImplementedError
        dir = QFileDialog.getExistingDirectory(self, "选取文件夹", "./")  # 起始路径
        if dir != "":

            print(f"We will boot Node in {dir}")
            try:
                os.chdir(dir)  # 切换目录
            except:
                print(f"We can't change Node path to {dir}")
                return

            self.NodeRootDir = dir
            self.DefaultWorkDirLabel.setText(f"默认工作路径为：{self.NodeRootDir}")

            cmd = f"cd {self.NodeRootDir}"

            self.OnlyDisplay(cmd)
            self.loadKeyandPassword()
        else:
            print(f"You cancel the folder selection, we will work in default dir:{self.NodeRootDir}")

    def loadKeyandPassword(self):

        keyname=f"{self.NodeRootDir}{os.sep}work{os.sep}key.json"
        with open(keyname, 'r') as f:
            data_check = json.load(f)

        if data_check!="":
            self.a1_Address=data_check[0]['Address']
            #self.entrustPass=data_check[0]['Password']
            self.entrustAccount.setText(self.a1_Address)
            self.WalletAddressLabel.setText("We will use default directory A1 address!")
            print("Use default key & password")

    # def OpenDirectory():
    #     directory1 = QFileDialog.getExistingDirectory(self,"选取文件夹", "./")  # 起始路径
    #     print(directory1)
    #     return directory1

    @pyqtSlot()
    def on_UseDefaultA1Account_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError

    @pyqtSlot()
    def on_NodeBootWalletAddress_editingFinished(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError

    @pyqtSlot()
    def on_NodeStartLogRefresh_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        # raise NotImplementedError
        self.NodeBootLogText.reload()
        ## should add some code here for server and client

    @pyqtSlot()
    def on_NodeServiceRefresh_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        # raise NotImplementedError
        output = "Refresh Finished ! Press button to Get more text!"

        self.NodeServiceText.append(output)

        self.NodeServiceText.reload()
        ## should add some code here for server and client

    @pyqtSlot()
    def on_CheckPunish_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError

    @pyqtSlot()
    def on_CheckNodeConnection_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError

    @pyqtSlot()
    def on_CheckNodeSyncNTP_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError

    @pyqtSlot()
    def on_CheckNodeSyncStatus_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError

    def DownloadFinish(self, msg):
        self.OnlyDisplay(f"auto download & Deploy gman! Msg is {msg}")

    @pyqtSlot()
    def on_DownloadTools_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        # raise NotImplementedError
        rootdir = os.getcwd()
        print(f"We will download all file in {rootdir}{os.sep}Download/ Directory")
        self.OnlyDisplay(f"autoDownloadGman {self.url}")

        self.DownloadThread.start()
        # 当获得循环完毕的信号时，停止计数
        self.DownloadThread.trigger.connect(self.DownloadFinish)

        # self.MainFile = autoDownloadGman(self.url)

        self.OnlyDisplay(f"autoDeployGman {self.MainFile}")
        # autoDeployGman(self.MainFile)

    @pyqtSlot()
    def on_GenerateEntrustFile_clicked(self):
        print("Generate Entrust file, it will open a dialog for entrust password input")
        if not self.checkGMAN():
            #os.chdir(self.NodeRootDir)
            return False

        gmandir = f"{os.getcwd()}"
        chaindatadir = f"{os.getcwd()}{os.sep}chaindata"
        gman=f"{gmandir}{os.sep}{self.browser.gmanName}"
        keyfile=f"{gmandir}{os.sep}key.json"
        entrustfile=f"{gmandir}{os.sep}entrust.json"

        if os.path.exists(entrustfile):
            postfix=datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            os.rename(entrustfile,f"{entrustfile}{postfix}")

        if self.checkboxManualConfigNode.checkState():
            ui = MATRIXPasswordDiaglog()
            ui.simplepassword.hide()
            r = ui.exec_()
            if not r:
                password="MATRIX$World@66#"
                print("We will use default Password")
            else:
                password=ui.text
        else:
            password="MATRIX$World#99!"

        # testmode parameter is not ok, therefore we must use pexpect
        cmd=f"{gman} --datadir {chaindatadir} aes --aesin {keyfile} --aesout {entrustfile} "

        child = GMANEntrustPexpect(cmd, password)

        # time.sleep(1)
        if os.path.exists(entrustfile):
            msg=f"Generating entrust file {entrustfile} successfully"
            QMessageBox.about(self, "通知", msg)

            self.entrustPass=password
        else:
            print("Can not find the entrust file")
            msg=f"没有生成entrust文件，请检查是否启动GMAN节点，输出日志为：{child.before}"
            QMessageBox.about(self, "通知", msg)

        self.OnlyDisplay(cmd,msg)
        # if self.grepMANAddress(line):
        #     print(f"Succussful generating A1 Address: {self.a1_Address}")
        #
        # else:
        #     QMessageBox.warning(self, "警告", f"检查是否启动GMAN节点，输出日志为：{line}")
        #     return False
        #
        os.chdir(self.NodeRootDir)

    @pyqtSlot()
    def on_CompileGAN_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError

    @pyqtSlot()
    def on_CheckGMANVersion_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError

    @pyqtSlot()
    def on_UploadLog_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError

    @pyqtSlot()
    def on_QPushButtonexecInputCMD_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        # raise NotImplementedError
        cmd = self.LineEditInput.text()
        print(f"We will execute the command {cmd} from line input line box")

        self.executeAndDisplay(cmd)

    @pyqtSlot()
    def on_OpenExplorer_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        # raise NotImplementedError

        url = "http://kfc.matrix.io"

        self.browser.openurl(url)
        self.OnlyDisplay(f"start {url}")
        # MATRIXWebutil.open_new(url)
        # MATRIXWebutil.open_new_tab(url)

    @pyqtSlot()
    def on_OpenExplorerWallet_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        # raise NotImplementedError
        url = "http://wallet.matrix.io"

        self.browser.openurl(url)
        self.OnlyDisplay(f"start {url}")

    @pyqtSlot()
    def on_OpenExplorerAccount_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        # raise NotImplementedError
        url = f"http://kfc.matrix.io/{self.a0_Address}"

        self.browser.openurl(url)
        self.OnlyDisplay(f"start {url}")

    @pyqtSlot()
    def on_DeployMinerNode_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        # raise NotImplementedError
        if not self.checkGMAN():
            #os.chdir(self.NodeRootDir)
            return False

        gmandir = f"{os.getcwd()}"
        chaindatadir = f"{os.getcwd()}{os.sep}chaindata"
        gman=f"{gmandir}{os.sep}{self.browser.gmanName}"
        #keyfile=f"{gmandir}{os.sep}key.json"
        entrustfile=f"{gmandir}{os.sep}entrust.json"

        if self.a1_Address=="":
            QMessageBox.about(self,"没有输入Address地址","Please Input A1 Address, don't leave it blank, you generate a new address!")
            return False

        if not MATRIXCmd.checkAddressValid(self.a1_Address):
            QMessageBox.about(self,"输入Address地址有误",f"Please Correct A1 Address:{self.a1_Address}, It contain Error!")
            return False

        if self.checkboxManualConfigNode.checkState():
            ui = ConfigNodeNormal()
            r=ui.exec_()
            if not r:
                print("you give up the configuration, and will use default parameter!")
                ServerArgs = f"{gman} --datadir {chaindatadir} --rpc --rpcaddr {self.rpcaddr} --rpccorsdomain '*' --networkid {self.networkID} --debug --verbosity {self.verbosityLevel} --manAddress {self.a1_Address} --entrust {entrustfile} --gcmode {self.gcmode} --outputinfo {self.output2File} --syncmode {self.syncmode}"
            else:
                self.output2File= ui.checkBoxDebug2File
                self.rpcaddr=ui.lineEditRPCAddress.text()
                self.networkID=ui.lineEditNetworkID.text()

                if ui.checkBoxGCMode.checkState():
                    self.gcmode="archive"
                else:
                    self.gcmode="none"

                self.verbosityLevel=ui.horizontalSliderDebugInfo.value()
                OtherPara=ui.lineEditOtherPara.text()

                if self.entrustPass == "":
                    # QMessageBox.about(self, "请手动输入entrust文件的password", f"Please Input entrust Password correctly!\n If It not ok!")

                    text, okPressed = QInputDialog.getText(self, "获取信息",
                                                           "请输入密码，一定输入委托加密密码，不是账户的密码\n，该密码包含各种特殊字符，输入不对，会不能启动节点",
                                                           QLineEdit.Normal)

                    if okPressed and text != "":
                        #self.entrustPass = text
                        print("We will use input password!")
                        ServerArgs = f"{gman} --datadir {chaindatadir} --rpc --rpcaddr {self.rpcaddr} --rpccorsdomain '*' --networkid {self.networkID} --debug --verbosity {self.verbosityLevel} --manAddress {self.a1_Address} --entrust {entrustfile} --gcmode {self.gcmode} --outputinfo {self.output2File} --syncmode {self.syncmode} {OtherPara} --tesmode {text}"
                    else:
                        print("No password! Node can't start!Maybe error")

                        ServerArgs = f"{gman} --datadir {chaindatadir} --rpc --rpcaddr {self.rpcaddr} --rpccorsdomain '*' --networkid {self.networkID} --debug --verbosity {self.verbosityLevel} --manAddress {self.a1_Address} --entrust {entrustfile} --gcmode {self.gcmode} --outputinfo {self.output2File} --syncmode {self.syncmode} {OtherPara} "
                else:
                    ServerArgs = f"{gman} --datadir {chaindatadir} --rpc --rpcaddr {self.rpcaddr} --rpccorsdomain '*' --networkid {self.networkID} --debug --verbosity {self.verbosityLevel} --manAddress {self.a1_Address} --entrust {entrustfile} --gcmode {self.gcmode} --outputinfo {self.output2File} --syncmode {self.syncmode} {OtherPara} --tesmode {self.entrustPass}"


        else:
            if self.entrustPass == "":

                ServerArgs = f"{gman} --datadir {chaindatadir} --rpc --rpcaddr {self.rpcaddr} --rpccorsdomain '*' --networkid {self.networkID} --debug --verbosity {self.verbosityLevel} --manAddress {self.a1_Address} --entrust {entrustfile} --gcmode {self.gcmode} --outputinfo {self.output2File} --syncmode {self.syncmode} "
            else:
                ServerArgs = f"{gman} --datadir {chaindatadir} --rpc --rpcaddr {self.rpcaddr} --rpccorsdomain '*' --networkid {self.networkID} --debug --verbosity {self.verbosityLevel} --manAddress {self.a1_Address} --entrust {entrustfile} --gcmode {self.gcmode} --outputinfo {self.output2File} --syncmode {self.syncmode} --testmode {self.entrustPass}"

        # testmode parameter is not ok, therefore we must use pexpect
        cmdorg = "gman --datadir chaindata --rpc --rpcaddr 0.0.0.0 --rpccorsdomain '*' --networkid 666 --debug --verbosity 5 --manAddress MAN.2UMgrmoFTq2urw1xKBgx5XfpFnhR3 --entrust entrust.json --gcmode archive --outputinfo 1 --syncmode full "


        print(ServerArgs)
        self.browser.saveExec(ServerArgs)

        self.NodeServiceText.append(f"在{os.getcwd()}下执行命令:\n{ServerArgs}\n请在窗口观察结果")
        QMessageBox.about(self, "MATRIX初始化节点状态",
                          f"执行命令为：{ServerArgs},执行结果请查看对应窗口，如果是MAC平台，请注意安装Xterm，或者在terminal窗口执行命令")

        os.chdir(self.NodeRootDir)

    @pyqtSlot()
    def on_ResetNode_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError

    @pyqtSlot()
    def on_NewNodeDepoly_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        # raise NotImplementedError
        print("We will deploy a new node, Nothing need to input!!")

        if not self.checkGMAN():
            #os.chdir(self.NodeRootDir)
            return False

        gmandir = f"{os.getcwd()}"
        chaindatadir = f"{os.getcwd()}{os.sep}chaindata"

        ServerArgs = f"{gmandir}{os.sep}{self.browser.gmanName} --datadir {chaindatadir} --rpc --rpcaddr 0.0.0.0 --rpccorsdomain '*' --networkid 1 --debug --verbosity 5 --gcmode archive --outputinfo 0 --syncmode full  "
        print(ServerArgs)
        self.browser.saveExec(ServerArgs)

        self.NodeServiceText.append(f"执行命令:{ServerArgs},请在窗口观察结果")
        QMessageBox.about(self, "MATRIX初始化节点状态",
                          f"执行命令为：{ServerArgs},执行结果请查看对应窗口，如果是MAC平台，请注意安装Xterm，或者在terminal窗口执行命令")

        os.chdir(self.NodeRootDir)

    def startThreadMonitor(self):
        self.NodeSubProcess.run()

    @pyqtSlot()
    def on_StopNode_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        # raise NotImplementedError
        print("We will kill all gman process!")
        reply = QMessageBox.question(self, '确认', '确认kill所有gman任务吗', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            autokillGman()
            self.OnlyDisplay("kill -9 |grep gman")
        else:
            print("Keep GMAN run.......!")

        cmd = "kill -9  `ps -ef | grep  -v grep  | grep  gman | grep 'networkid'  | awk '{print $2}'`"
        self.executeAndDisplay(cmd)

    @pyqtSlot()
    def on_TransferCash_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError

    @pyqtSlot()
    def on_pushButtonClearLineInput_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        # raise NotImplementedError
        print("clear command line input!")
        self.LineEditInput.clear()
        self.LineEditInput.setText("")
        self.LineEditInput.setFocus()

    @pyqtSlot()
    def on_pushButtonAbout_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        # raise NotImplementedError
        helpurl = "http://www.matrix.io/help"
        helpmsg = f"We will Display the help dialog Box! If you are new node, just deploy with download/init site/start " \
            f"a node step!\nIf you have a deposit, please deploy with the following step:\n1.generate a random " \
            f"deposit accout.\n2.signature it with password.\n3.deploy this account! "
        self.OnlyDisplay(f"Open Help mainpage {helpurl}", helpmsg)
        QMessageBox.about(self, "MATRIX Node Help", f"Please visit {helpurl} to get more information")
        self.browser.openurl(helpurl)

    def executeAndDisplay(self, cmd):
        print(f"Run Cmd:\n{cmd}")
        # localargs = shlex.split(cmd)
        #
        # for s in localargs :
        #    print(f"part {s}\n")
        #
        # if not os.path.exists(localargs[0]):
        #    result=f"error! file {localargs[0]} not exists!"
        #    print(result)
        #    self.cmdResult = result
        #    return False

        # try:
        #    f = open(localargs[0])
        #    f.close()
        # except IOError:
        #    result = f"Error in change directory or File doesn't exist! You should change to correct Path which contain {localargs[0]}"
        #    print(result)
        #    self.cmdResult=result
        #    return False

        child1 = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                  stdin=subprocess.PIPE)
        # child1 = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

        outs, errs = child1.communicate()

        # output=str(outs).decode('string_escape')
        output = str(outs, 'utf-8')
        print(f"cmd execute result:\n{output}")

        self.cmdLogText.setPlainText(cmd)

        num = self.listWidget.count()
        if num > self.listlimited:
            print("too much item, we save it into cmd result history, Please open cmd.log!")

            with open('cmd.log', 'a') as f:
                for i in range(num):
                    logtext = self.listWidget.item(i).text()
                    f.write(logtext)

            self.listWidget.clear()
        #     self.listWidget.addItem(innercmd)
        # else:
        #     self.listWidget.addItem(innercmd)

        self.cmdNum = self.cmdNum + 1
        self.listWidget.addItem(f"{self.cmdNum}:{cmd}")
        self.NodeBootLogText.append(f"CMD {self.cmdNum} result:\n{output}\n++++++++ output Finished!\n")
        self.cmdResult = output
        self.NodeBootLogText.show()
        return output

    def OnlyDisplay(self, cmd, output=""):
        print("We will run python internal cmd")
        innercmd = f"python MATRIXNode.py {cmd}"
        if output == "":
            output = f"Run in console and see the result\n{innercmd}\n"

        self.cmdLogText.setPlainText(innercmd)
        num = self.listWidget.count()
        if num > self.listlimited:
            print("too much item, we save it into cmd result history, Please open cmd.log!")

            with open('cmd.log', 'a') as f:
                for i in range(num):
                    logtext = self.listWidget.item(i).text()
                    f.write(logtext)

            self.listWidget.clear()
        #     self.listWidget.addItem(innercmd)
        # else:
        #     self.listWidget.addItem(innercmd)

        # self.listWidget.addItem(innercmd)
        # self.NodeBootLogText.append(output)

        self.cmdNum = self.cmdNum + 1
        self.listWidget.addItem(f"{self.cmdNum}:{innercmd}")
        self.NodeBootLogText.append(f"CMD {self.cmdNum} result:\n{output}\n++++++++ output Finished!\n")
        self.NodeBootLogText.show()

    def update_Node_info(self, data):
        """更新内容"""
        # self.setItem(0, 0, QTableWidgetItem(data))  # 设置表格内容(行， 列) 文字
        self.NodeServiceText.append(data)


class DisplaySubProcessInfoThread(QThread):
    # 定义一个信号
    trigger = pyqtSignal(str)
    tt = 0

    def __int__(self, cmd="", parent=None):
        # 初始化函数，默认
        super(DisplaySubProcessInfoThread, self).__init__()
        self.cmd = cmd
        print(f"exec command {self.cmd}")

    def run(self):
        self.sleep(1)
        # 等待5秒后，给触发信号，并传递test
        self.tt = self.tt + 1
        msg = f"{self.cmd} thread time {self.tt}"
        print(msg)
        self.trigger.emit(msg)


class DownloadThread(QThread):
    # 定义一个信号
    trigger = pyqtSignal(str)
    url = 'https://www.matrix.io/downloads/'
    MainFile = './gman'

    def __int__(self, myurl='https://www.matrix.io/downloads/', parent=None):
        # 初始化函数，默认
        super(DownloadThread, self).__init__()
        print(f"Download GMAN file from {myurl}....")
        self.url = myurl

    def run(self):
        msg = f"download GMAN from {self.url}"
        print(msg)
        self.MainFile = autoDownloadGman(self.url)
        msg = f"Deploy {self.MainFile}"
        print(msg)
        autoDeployGman(self.MainFile)

        self.trigger.emit(msg)


if __name__ == "__main__":
    fire.Fire()
    app = QApplication(sys.argv)
    ui = MainWindow()

    sys.exit(app.exec_())
