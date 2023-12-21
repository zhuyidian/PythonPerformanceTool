import sys
from PyQt5.QtWidgets import QWidget,QLabel, QPushButton,QCheckBox, QApplication
from PyQt5.QtGui import QIcon ,QFont

# class Example(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.initUI()
#
#     def initUI(self):
#         btn1 = QPushButton("按钮1", self)
#         btn1.move(30, 50)
#         btn2 = QPushButton("按钮2", self)
#         btn2.setIcon(QIcon('bitbug.ico'))
#         btn2.move(150, 50)
#         btn1.clicked.connect(self.buttonClicked)  #绑定信号
#         btn2.clicked.connect(self.buttonClicked)
#
#         self.setGeometry(300, 300, 390, 350)
#         self.setWindowTitle('QPushButton')
#         self.show()
#
#     def buttonClicked(self):
#         print(self.sender())
#         print(self.sender().text() + '被按下')


import  random
class game(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.result = QLabel(self)
        self.result.setText('结局一片空白')
        self.result.setFont(QFont('microsoft Yahei', 20))  #字体格式
        self.result.move(80,150)
        btn1 = QPushButton("剪子", self)
        btn1.setIcon(QIcon('剪子.png'))
        btn1.setStyleSheet("QPushButton{background:yellow}")
        btn1.move(30, 50)
        btn2 = QPushButton("包子", self)
        btn2.setIcon(QIcon('包子.png'))
        btn2.move(150, 50)
        btn3 = QPushButton("锤子", self)
        btn3.setIcon(QIcon('锤子.png'))
        btn3.move(250, 50)

        btn1.clicked.connect(self.buttonClicked)  #绑定信号
        btn2.clicked.connect(self.buttonClicked)
        btn3.clicked.connect(self.buttonClicked)
        self.setGeometry(300, 300, 390, 350)
        self.setWindowIcon(QIcon('剪子.png'))
        self.setWindowTitle('猜丁克')
        self.show()

    def buttonClicked(self):
        ls = ['剪子','包子','锤子']
        print(self.sender())
        # self.statusBar().showMessage(self.sender.text() + ' was pressed')
        print(self.sender().text() + '被按下')
        a = random.choice(ls)
        if a == self.sender().text():
            self.result.setText('平局')
        if a != self.sender().text():
            self.result.setText('请同学们补充')
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = game()
    sys.exit(app.exec_())