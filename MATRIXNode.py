# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""

from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from MATRIXCmd import *
from MATRIXStringTools import *
# from PyQt5.QtWidgets import QMainWindow
# from PyQt5.QtCore import pyqtSlot
from Ui_MATRIXNode import Ui_MainWindow
from MATRIXFileTools import *

class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    vdepositValue = 0
    mdepositValue = 0
    transferValue = 0

    a0_Address = ""
    a1_Address = ""
    transfer_Address=""
    superNode_Address=""

    fixedPeriod = "活期"
    select_VM = "Miner"
    select_actor = "SuperNode"
    NodeRootDir=f".{os.sep}"

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
            #self.WalletAddress.setFocus()
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
        #raise NotImplementedError
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
        #raise NotImplementedError
        print("Select Validator.")
        self.select_VM="Validator"
        self.mdepositValue = 0
        self.MDepositValue.clear()
        self.VDepositValue.setFocus()

    @pyqtSlot()
    def on_MinerradioButton_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        #raise NotImplementedError
        print("Select Miner.")
        self.select_VM="Miner"
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
        #raise NotImplementedError
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
        #raise NotImplementedError
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
        raise NotImplementedError


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

    @pyqtSlot()
    def on_GenerateRandomAccountAddress_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError

    @pyqtSlot()
    def on_NodeInit_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        #raise NotImplementedError


    @pyqtSlot()
    def on_GenerateRandomAccountAddress_2_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError


    @pyqtSlot()
    def on_SetDefaultWorkDir_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        #raise NotImplementedError
        dir= QFileDialog.getExistingDirectory(self,"选取文件夹", "./")  # 起始路径
        if dir != "":

            print(f"We will boot Node in {dir}")
            try:
                os.chdir(dir)  # 切换目录
            except:
                print(f"We can't change Node path to {dir}")
                return

            self.NodeRootDir = dir
            self.DefaultWorkDirLabel.setText(f"默认工作路径为：{self.NodeRootDir}")
        else:
            print(f"You cancel the folder selection, we will work in default dir:{self.NodeRootDir}")


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
        raise NotImplementedError

    @pyqtSlot()
    def on_NodeServiceRefresh_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError

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

    @pyqtSlot()
    def on_DownloadTools_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError

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
    def on_OpenExplorer_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError

    @pyqtSlot()
    def on_OpenExplorerWallet_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError

    @pyqtSlot()
    def on_OpenExplorerAccount_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError

    @pyqtSlot()
    def on_DeployMinerNode_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError

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
        raise NotImplementedError

    @pyqtSlot()
    def on_StopNode_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError

    @pyqtSlot()
    def on_TransferCash_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = MainWindow()

    sys.exit(app.exec_())
