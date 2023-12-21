import sys
from PyQt5.QtWidgets import QWidget, QLabel, QFocusFrame,QApplication
from PyQt5.QtGui import QPixmap

class Tip(QWidget):
    def __init__(self,tip):
        super().__init__()
        self.tip = tip
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Tip')
        self.a = QLabel(self)
        self.a.setToolTip('xxx')
        # info = input('请输入标签信息：')
        self.a.setText(self.tip)   #也可以通过input传递信息
        self.a.move(130,100)
        # print(self.a.text())
        b = QLabel(self)
        b.setPixmap(QPixmap('bitbug.ico'))
        b.move(100,80)
        self.show()

def show(tip):
    global app
    app = QApplication(sys.argv)
    a = Tip(tip)
    sys.exit(app.exec_())

if __name__ == "__main__":
    show("OK")