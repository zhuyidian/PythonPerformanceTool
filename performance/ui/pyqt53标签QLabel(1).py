import sys
from PyQt5.QtWidgets import QWidget, QLabel, QApplication
from PyQt5.QtGui import QPixmap
class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('QLabel标签')
        self.a = QLabel(self)
        self.a.setToolTip('气泡提示')
        # info = input('请输入标签信息：')
        self.a.setText('道东偶尔 ')   #也可以通过input传递信息
        self.a.move(50,50)
        print(self.a.text())
        b = QLabel(self)
        b.setPixmap(QPixmap('bitbug.ico'))
        b.move(100,100)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())