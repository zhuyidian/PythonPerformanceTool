from PyQt5.QtWidgets import QWidget, QPushButton, QFrame, QApplication
import sys

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        redb = QPushButton('Red', self)
        redb.setCheckable(True)  #按钮变为可切换按钮
        redb.move(10, 10)
        redb.clicked.connect(self.setColor)
        greenb = QPushButton('Green', self)
        greenb.setCheckable(True)
        greenb.move(10, 60)
        greenb.clicked.connect(self.setColor)
        blueb = QPushButton('Blue', self)      #也可以设置背景颜色
        blueb.setCheckable(True)
        blueb.move(10, 110)
        blueb.clicked.connect(self.setColor)
        self.square = QFrame(self)   #创建一个方框
        self.square.setGeometry(150, 20, 100, 100)
        self.square.setStyleSheet("QFrame{background-color: black }" )  #设置图形界面的外观
        self.setGeometry(300, 300, 280, 170)
        self.setWindowTitle('切换按钮')
        self.show()

    def setColor(self):
        source = self.sender()
        if source.text() == "Red":
            self.square.setStyleSheet("QFrame{background-color: Red }")
        if source.text() == "Green":
            self.square.setStyleSheet("QFrame{background-color: Green }")
        if source.text() == "Blue":
            self.square.setStyleSheet("QFrame{background-color: Blue }")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())