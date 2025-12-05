import sys
from PyQt5.QtWidgets import QApplication, QPushButton,QWidget,QProgressBar
from PyQt5.QtCore import QBasicTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QCoreApplication

app = None

class ProgressWindow(QWidget):
    def __init__(self,total_time):
        super().__init__()
        self.total_time = total_time
        self.step_value = int((1 / (100 / total_time)) * 1000)
        print(f'total_time={self.total_time},step_value={self.step_value}')
        self.initUI()

    def initUI(self):
        #进度条设置
        self.pbar = QProgressBar(self)  #此除的self是否可以不用
        self.pbar.setGeometry(30,50,520,25)
        #按键
        # self.btn = QPushButton("开始",self)
        # self.btn.move(50,90)
        #按键连接事件
        # self.btn.clicked.connect(self.doAction)
        #时间模块
        self.timer = QBasicTimer()
        # 计数
        self.step = 0
        self.setGeometry(500,500,580,150)
        self.setWindowTitle("系统资源抓取")
        self.setWindowIcon(QIcon('chaoxiang.jpg'))
        self.show()

    """
    total_time = 10S
    num = 100
    1 / ? = 100 / 10
    ? = 1 / 100 / 10
    """
    def timerEvent(self, *args, **kwargs):
        if self.step >= 100:
            self.timer.stop()
            # self.btn.setText("完成")
            self.close()
            QCoreApplication.instance().quit
            return
        self.step = self.step + 1
        self.pbar.setValue(self.step)

    def doAction(self):
        if self.timer.isActive():
            self.timer.stop()
            # self.btn.setText("开始")
        else :
            self.timer.start(self.step_value,self)
            # self.btn.setText("停止")

def show(total_time):
    global app
    app = QApplication(sys.argv)
    a = ProgressWindow(total_time)
    a.doAction()
    sys.exit(app.exec_())

# def close():
#     QCoreApplication.instance().quit

if __name__ == "__main__":
    show(60)
