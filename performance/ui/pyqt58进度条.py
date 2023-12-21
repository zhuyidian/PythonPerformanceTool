from PyQt5.QtWidgets import (QWidget, QProgressBar,
    QPushButton, QApplication)
from PyQt5.QtCore import QBasicTimer
import sys

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.pbar = QProgressBar(self)    #创建了一个水平的进度条
        self.pbar.setGeometry(30, 40, 200, 25)
        self.pbar.setValue(10)              #设置进度条数值
        self.btn = QPushButton('Start', self)
        self.btn.move(40, 80)
        self.btn.clicked.connect(self.doAction)
        self.timer = QBasicTimer()
        self.step = 0
        self.setGeometry(300, 300, 280, 170)
        self.setWindowTitle('进度条')
        self.show()

    def timerEvent(self, e):    #时钟
        if self.step >= 100:
            self.timer.stop()
            self.btn.setText('Finished')
            return
        self.step = self.step + 1
        self.pbar.setValue(self.step)

    def doAction(self):
        if self.timer.isActive():  #检查时钟是否被激活，激活状态为真，否则为假
            self.timer.stop()      #时钟停止
            self.btn.setText('Start')
        else:
            self.timer.start(100, self)   #时钟开始，产生100个信号源，每个信号0.1秒
            self.btn.setText('Stop')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())