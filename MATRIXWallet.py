# !/usr/bin/python
# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import *

from Ui_MATRIXWallet import Ui_MainWindow

from MATRIXCmd import *


class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    A0_Address = ""
    A1_Address = ""
    Man = MATRIXCmd()

    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.show()
        self.cmdNum = 0
        self.cmdErrNum = 0
        self.cmdLog = ""
        self.cmdErrLog = ""

    def closeEvent(self, event):
        reply = QMessageBox.question(self, '确认', '确认退出吗', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    @pyqtSlot()
    def on_NewNodeDepoly_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        # raise NotImplementedError
        # QMessageBox.about(self,self.WorkAccount.text(), 'Good!')
        address = self.WorkAccount.text()
        match, valid_address = MATRIXCmd.checkAddressValid(address)

        if match:
            # 使用Match获得分组信息
            print("A1 account Ok.")
            self.WorkAccountLabel.setText('A1账户正常')
            self.A1_Address = valid_address
            depoly_msg = '部署账户为：' + valid_address
            QMessageBox.question(self, '提示部署输入账户为', depoly_msg, QMessageBox.Yes | QMessageBox.No,
                                 QMessageBox.No)
        else:
            self.WorkAccountLabel.setText('A1账户不正常，格式为MAN.XXXXX')
            print("A1 account Error.")

            QMessageBox.about(self, '提示请勿输入A0账户', '请输入正确的MATRIX A1账户,单纯部署无需输入A0账户')
            self.WorkAccount.clear()
            self.WorkAccount.setFocus()
            return

        cmd = 'ls'
        return_code, out = MATRIXCmd.execute_cmd(cmd)
        self.cmdNum = self.cmdNum + 1
        #tmpText = self.cmdLogText.getPaintContext()
        tmpText = f"\n{self.cmdNum}:{cmd}"

        self.cmdLogText.appendPlainText(tmpText)
        self.cmdLog = out

        if return_code != 0:
            # raise SystemExit('execute {0} err :{1}'.format(cmd, out))
            print("execute {0} err :{1}".format(cmd, out))
            self.cmdErrNum = self.cmdErrNum + 1
            self.cmdErrLog = out

        else:
             print("execute command ({0} sucessful)".format(cmd))

        self.StatusLogText.setPlainText(f'{self.cmdLog}')

    # guessnumber = 10
    # int(self.WorkAccount.text())

    # print(self.num)
    # raise NotImplementedError

    @pyqtSlot()
    def on_WorkAccount_editingFinished(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        # raise NotImplementedError
        address = self.WorkAccount.text()
        match, valid_address = MATRIXCmd.checkAddressValid(address)
        if match:
            # 使用Match获得分组信息
            print("A1 account Ok.")
            self.WorkAccountLabel.setText('A1账户正常')
            self.A1_Address = valid_address
        else:
            self.WorkAccountLabel.setText('A1账户不正常，格式为MAN.XXXXX')
            print("A1 account Error.")
            self.WorkAccount.clear()
            self.WorkAccount.setFocus()

    @pyqtSlot()
    def on_CheckGMANVersion_clicked(self):
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
    def on_OpenExplorer_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError

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
            print("A0 account Ok.")
            self.WalletAddressLabel.setText('A0账户格式正常，但只有启动抵押和钱包功能时，才需要输入')
        else:
            self.WalletAddressLabel.setText('A0账户格式不正常，格式为MAN.XXXXX，')
            print("A0 account Error.")
            self.WalletAddress.clear()
            # self.WalletAddress.setFocus()

    @pyqtSlot()
    def on_VDepositValue_editingFinished(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError

    @pyqtSlot()
    def on_MinerradioButton_clicked(self):
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
        raise NotImplementedError

    @pyqtSlot()
    def on_MDepositValue_editingFinished(self):
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
    def on_CheckNodeSyncStatus_clicked(self):
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
    def on_Deposit_clicked(self):
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
    def on_DecreaseDeposit_clicked(self):
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
    def on_CompileGAN_clicked(self):
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
        raise NotImplementedError

    @pyqtSlot()
    def on_CurrentradioButton_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError

    @pyqtSlot()
    def on_Fixed1mradioButton_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError

    @pyqtSlot()
    def on_Fixed3MradioButton_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError

    @pyqtSlot()
    def on_Fixed6MradioButton_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError

    @pyqtSlot()
    def on_Fixed12Mradiobutton_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError

    @pyqtSlot()
    def on_Current2Fixed_clicked(self):
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
    def on_ResetNode_2_clicked(self):
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
    def on_CheckNodeSyncNTP_clicked(self):
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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = MainWindow()

    sys.exit(app.exec_())
