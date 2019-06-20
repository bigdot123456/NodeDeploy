import sys
import time

from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer, QThread, pyqtSignal
from Ui_MATRIXNode import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        self.setupUi(self)
        # 初始化一个定时器
        self.timer = QTimer(self)
        # 定义时间超时连接start_app
        self.timer.timeout.connect(self.start)
        # 定义时间任务是一次性任务
        self.timer.setSingleShot(False)
        # 启动时间任务
        self.timer.start()
        # 实例化一个线程
        self.work = WorkThread()
        # 多线程的信号触发连接到UpText
        self.work.trigger.connect(self.UpText)

    def start(self):
        # time.sleep(2)
        # self.textBrowser.append('test1')
        # 启动另一个线程
        self.work.run()

    def UpText(self, str):
        #time.sleep(2)
        self.NodeServiceText.append(str)


class WorkThread(QThread):
    # 定义一个信号
    trigger = pyqtSignal(str)
    tt=0

    def __int__(self):
        # 初始化函数，默认
        super(WorkThread, self).__init__()

    def run(self):
        time.sleep(1)
        # 等待5秒后，给触发信号，并传递test
        self.tt=self.tt+1
        msg=f"thread time {self.tt}"
        print(msg)
        self.trigger.emit(msg)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
