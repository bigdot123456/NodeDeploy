# coding=utf-8

'''
密码输入框demo
'''

import sys
import re

from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QKeyEvent, QKeySequence
from PyQt5.QtWidgets import QDialog, QApplication, QLineEdit, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, \
    QMessageBox, QCheckBox
from PyQt5.QtWidgets import (QWidget)


# coding=utf-8


class MATRIXPasswordDiaglog(QDialog):
    '''
    我们自己的密码输入框
    '''

    def __init__(self):
        '''
        一些初始设置
        '''
        super().__init__()
        self.initUI()

    def initUI(self):
        '''
        界面初始设置
        '''
        self.resize(350, 100)
        self.setWindowTitle("密码输入框")

        self.lb = QLabel("请输入密码：", self)
        self.lbok = QLabel("等待输入密码状态", self)

        self.edit = QLineEdit(self)
        self.edit.installEventFilter(self)  # 输入框安装事件过滤器

        self.lb1 = QLabel("请再次输入密码：", self)
        self.edit1 = QLineEdit(self)
        self.edit1.installEventFilter(self)  # 输入框安装事件过滤器

        self.bt1 = QPushButton("确定", self)
        self.bt2 = QPushButton("取消", self)
        self.viewpassword = QCheckBox("明文显示密码", self)
        self.simplepassword = QCheckBox("我嫌麻烦，不考虑安全性，就用简单密码", self)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.bt1)
        hbox.addStretch(1)
        hbox.addWidget(self.bt2)
        hbox.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addWidget(self.lbok)
        vbox.addWidget(self.lb)
        vbox.addWidget(self.edit)
        vbox.addWidget(self.lb1)
        vbox.addWidget(self.edit1)
        vbox.addWidget(self.viewpassword)
        vbox.addWidget(self.simplepassword)

        vbox.addStretch(1)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        self.edit.setContextMenuPolicy(Qt.NoContextMenu)  # 不允许出现上下文菜单
        self.edit.setPlaceholderText("密码不超16位，最低8位，必须包含大小写和特殊字符")  # 输入密码前可以看到一些小提示信息，这个非常实用。
        self.edit.setEchoMode(QLineEdit.Password)  # 加密显示输入内容

        self.edit1.setContextMenuPolicy(Qt.NoContextMenu)  # 不允许出现上下文菜单
        self.edit1.setPlaceholderText("密码8~16位长度，必须包含大小写和特殊字符")  # 输入密码前可以看到一些小提示信息，这个非常实用。
        self.edit1.setEchoMode(QLineEdit.Password)  # 加密显示输入内容

        self.edit.editingFinished.connect(self.checkPasswordValid)

        # 将密码输入框设置为仅接受符合验证器条件的输入

        self.bt1.clicked.connect(self.Ok)
        self.bt2.clicked.connect(self.Cancel)

        self.viewpassword.clicked.connect(self.ViewPassword)

        # object = QObject()

    def checkPasswordValid(self):
        # regx = QRegExp("^[a-zA-Z][0-9A-Za-z]{14}$")
        # regx = QRegExp("^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{16}$")

        # 构建一个正则表达式：
        # 1、长度不能8～16位；
        # 2、符号由数字,大写字母,小写字母,特殊符,至少其中三种组成；

        if self.simplepassword.checkState():
            self.lbok.setText("You will use simple Password, we will not check it")
        else:
            line = self.edit.text()

            # matchObj = re.match(r'^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{8,16}$', line, re.M | re.I)

            matchObj = re.match(r"^.*(?=.{6,16})(?=.*\d)(?=.*[A-Z]{2,})(?=.*[a-z]{2,})(?=.*[!@#$%^&*?\(\)]).*$", line)

            if matchObj:
                msg="设置密码合格，符号包含了至少1个数字,2大写字母,2小写字母,1个特殊符组成"
                print(msg)
                self.lbok.setText(msg)
                # matchObj.group()
                return True
            else:
                msg="密码不符合要求，符号至少由1个数字,2大写字母,2小写字母,1个特殊符组成"
                print(f"密码不合格!{line}")
                self.lbok.setText(msg)
                # QMessageBox.warning(self, "警告", msg)
                return False

        # 构造一个验证器，QLineEdit对象接受与正则表达式匹配的所有字符串。匹配是针对整个字符串。

        # self.edit1.setValidator(validator1)

    def eventFilter(self, object, event):
        '''
        鼠标移动对应的事件类型为QEvent.MouseMove，
        鼠标双击对应的事件类型为QEvent.MouseButtonDblClick，
        全选、复制、粘贴对应的事件类型为 QEvent.KeyPress，当接收到这些事件时，需要被过滤掉，返回true。
        '''
        if object == self.edit:
            if event.type() == QEvent.MouseMove or event.type() == QEvent.MouseButtonDblClick:
                return True
            elif event.type() == QEvent.KeyPress:
                key = QKeyEvent(event)
                if key.matches(QKeySequence.SelectAll) or key.matches(QKeySequence.Copy) or key.matches(
                        QKeySequence.Paste):
                    return True
        return QDialog.eventFilter(self, object, event)  # 继续传递该事件到被观察者，由其本身调用相应的事件

    def Ok(self):
        '''
        结束对话框返回1
        '''
        self.text = self.edit.text()
        self.text1 = self.edit1.text()

        if self.text != self.text1:
            QMessageBox.warning(self, "警告", "前后两次密码不一致")
        else:

            if len(self.text) == 0:
                QMessageBox.warning(self, "警告", "密码为空")
            elif len(self.text) < 8:
                QMessageBox.warning(self, "警告", "密码长度低于8位")
            elif self.simplepassword.checkState() or self.checkPasswordValid():
                self.done(1)

    def Cancel(self):
        '''
        结束对话框返回0
        '''
        self.done(0)

    def ViewPassword(self):
        '''
        查看密码
        :return:
        '''
        if self.viewpassword.checkState():
            self.edit.setEchoMode(QLineEdit.Normal)
            self.edit1.setEchoMode(QLineEdit.Normal)
        else:
            self.edit.setEchoMode(QLineEdit.Password)
            self.edit1.setEchoMode(QLineEdit.Password)


class Example(QWidget):
    '''
    DIY密码输入框
    '''

    def __init__(self):
        '''
        一些初始设置
        '''
        super().__init__()
        self.initUI()

    def initUI(self):
        '''
        界面初始设置
        '''
        self.resize(380, 180)
        self.setWindowTitle('MATRIX密码输入对话框')

        self.lb1 = QLabel('密码在此显示...', self)
        self.lb1.move(20, 20)

        self.bt3 = QPushButton('请输入密码', self)
        self.bt3.move(20, 140)

        self.show()

        self.bt3.clicked.connect(self.showDialog)

    def showDialog(self):
        '''
        当我们输入密码的时候，会有不同的显示
        '''
        sender = self.sender()
        if sender == self.bt3:
            pwd = MATRIXPasswordDiaglog()  # DIY密码输入框
            r = pwd.exec_()  # 执行密码输入框
            if r:
                self.lb1.setText(pwd.text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
