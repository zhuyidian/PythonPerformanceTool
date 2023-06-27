import sys
from PyQt5.QtWidgets import QApplication, QPushButton,QWidget,QProgressBar
from PyQt5.QtCore import QBasicTimer
from PyQt5.QtGui import QIcon

class example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        #进度条设置
        self.pbar = QProgressBar(self)  #此除的self是否可以不用
        self.pbar.setGeometry(30,50,200,25)
        #按键
        self.btn = QPushButton("开始",self)
        self.btn.move(50,90)
        #按键连接事件
        self.btn.clicked.connect(self.doAction)
        #时间模块
        self.timer = QBasicTimer()
        # 计数
        self.step = 0
        self.setGeometry(500,500,580,370)
        self.setWindowTitle("自习室收费系统")
        self.setWindowIcon(QIcon('chaoxiang.jpg'))
        self.show()

    def timerEvent(self, *args, **kwargs):
        if self.step >= 100:
            self.timer.stop()
            self.btn.setText("完成")
            return
        self.step = self.step + 1
        self.pbar.setValue(self.step)
    def doAction(self):
        if self.timer.isActive():
            self.timer.stop()
            self.btn.setText("开始")
        else :
            self.timer.start(100,self)
            self.btn.setText("停止")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    a = example()
    sys.exit(app.exec_())
