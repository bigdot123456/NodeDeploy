# -*- coding: utf-8 -*-

"""
Module implementing ConfigNodeNormal.
"""

import fire
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog

from Ui_NodeConfig import Ui_ConfigNodeNormal


class ConfigNodeNormal(QDialog, Ui_ConfigNodeNormal):
    """
    Class documentation goes here.
    """
    networkID = 1
    verbosityLevel = 3
    output2File = 0
    rpcaddr = "0.0.0.0"
    syncmode = "full"
    gcmode = "archive"
    lessdisk=0
    otherPara=""

    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(ConfigNodeNormal, self).__init__(parent)
        self.setupUi(self)

    @pyqtSlot(int)
    def on_horizontalSliderDebugInfo_valueChanged(self, value):
        """
        Slot documentation goes here.
        
        @param value DESCRIPTION
        @type int
        """
        # TODO: not implemented yet
        # raise NotImplementedError
        self.verbosityLevel = value
        self.lineEditOtherPara.clear()

    @pyqtSlot(int)
    def on_horizontalSliderDebugInfo_actionTriggered(self, action):
        """
        Slot documentation goes here.
        
        @param action DESCRIPTION
        @type int
        """
        # TODO: not implemented yet
        # raise NotImplementedError
        print(f"We use self.verbosityLevel with {self.verbosityLevel}")


    @pyqtSlot()
    def on_checkBoxDebug2File_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        #raise NotImplementedError
        if self.checkBoxDebug2File.checkStateSet():
            self.Debug2File = 1
        else:
            self.Debug2File=0

    @pyqtSlot()
    def on_checkBoxGCMode_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        #raise NotImplementedError

        if self.checkBoxGCMode.checkState():
            self.gcmode = "archive"
        else:
            self.gcmode = "memory"

    @pyqtSlot()
    def on_checkBoxSyncmode_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        #raise NotImplementedError
        if self.checkBoxSyncmode.checkState():
            self.syncmode="full"
        else:
            self.syncmode="half"

    @pyqtSlot()
    def on_checkBoxLessDisk_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        # raise NotImplementedError
        if self.checkBoxLessDisk.checkState():
            self.lessdisk=1
        else:
            self.lessdisk=0

    @pyqtSlot()
    def on_buttonBox_accepted(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        # raise NotImplementedError
        return True

    @pyqtSlot()
    def on_buttonBox_rejected(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        # raise NotImplementedError
        return False

    def is_number(self,s):
        try:
            int(s)
            return True
        except ValueError:
            pass

        try:
            import unicodedata
            unicodedata.numeric(s)
            return False
        except (TypeError, ValueError):
            pass

        return False

    @pyqtSlot()
    def on_lineEditNetworkID_editingFinished(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        # raise NotImplementedError
        line = self.lineEditNetworkID.text()
        if self.is_number(line):
            self.networkID = int(line)
        else:
            self.networkID = 1
            self.lineEditNetworkID.setText("1")

    @pyqtSlot()
    def on_lineEditRPCAddress_editingFinished(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        #raise NotImplementedError
        line = self.lineEditRPCAddress.text()
        if self.isIpV4AddrLegal(line):
            self.rpcaddr=line
        else:
            self.rpcaddr = "0.0.0.0"
            self.lineEditRPCAddress.setText(self.rpcaddr)

    def isIpV4AddrLegal(self,ipStr):
        # 切割IP地址为一个列表
        ip_split_list = ipStr.strip().split('.')
        # 切割后列表必须有4个元素
        if 4 != len(ip_split_list):
            return False
        for i in range(4):
            try:
                # 每个元素必须为数字
                ip_split_list[i] = int(ip_split_list[i])
            except:
                print(f"IP invalid:{ipStr}")
                return False
        for i in range(4):
            # 每个元素值必须在0-255之间
            if ip_split_list[i] <= 255 and ip_split_list[i] >= 0:
                pass
            else:
                print(f"IP invalid:{ipStr}")
                return False

        return True

    @pyqtSlot()
    def on_lineEditOtherPara_editingFinished(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        #raise NotImplementedError
        self.otherPara=self.lineEditOtherPara.text()
        print(f"You should check parameter {self.otherPara}")

    @pyqtSlot()
    def on_pushButtonPastPara_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        # raise NotImplementedError
        print("!!! not implemented yet")


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    fire.Fire()

    ui = ConfigNodeNormal()

    ui.show()

    sys.exit(app.exec_())
