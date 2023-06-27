import sys
from PyQt5.QtWidgets import QWidget, QLabel,QLineEdit,QApplication

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 500, 300)
        self.setWindowTitle('文本框')
        a = QLabel(self)
        a.setText('用户名：')
        a.move(40,102)
        b = QLineEdit(self)
        # print(b.text())
        b.setPlaceholderText('请输入用户名')   #设置文本框浮现文字
        b.move(100,100)
        c = QLabel(self)
        c.setText('密码：')
        c.move(40, 152)
        d = QLineEdit(self)
        d.setPlaceholderText('请输入6位数密码')
        d.move(100, 150)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())