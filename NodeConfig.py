# -*- coding: utf-8 -*-

"""
Module implementing ConfigNodeNormal.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog

from PyQt5 import QtCore, QtGui, QtWidgets

from Ui_NodeConfig import Ui_ConfigNodeNormal
import fire

class ConfigNodeNormal(QDialog, Ui_ConfigNodeNormal):
    """
    Class documentation goes here.
    """
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
        raise NotImplementedError
    
    @pyqtSlot(int)
    def on_horizontalSliderDebugInfo_actionTriggered(self, action):
        """
        Slot documentation goes here.
        
        @param action DESCRIPTION
        @type int
        """
        # TODO: not implemented yet
        raise NotImplementedError
    
    @pyqtSlot()
    def on_checkBoxDebug2File_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError
    
    @pyqtSlot()
    def on_checkBoxGCMode_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError
    
    @pyqtSlot()
    def on_checkBoxSyncmode_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError
    
    @pyqtSlot()
    def on_checkBoxLessDisk_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError
    
    @pyqtSlot()
    def on_buttonBox_accepted(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError
    
    @pyqtSlot()
    def on_buttonBox_rejected(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError
    
    @pyqtSlot()
    def on_lineEditNetworkID_editingFinished(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError
    
    @pyqtSlot()
    def on_lineEditRPCAddress_editingFinished(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError
    
    @pyqtSlot()
    def on_lineEditOtherPara_editingFinished(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError
    
    @pyqtSlot()
    def on_pushButtonPastPara_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    
    fire.Fire()
 
    ui = ConfigNodeNormal()
    
    ui.show()

 
    sys.exit(app.exec_())
