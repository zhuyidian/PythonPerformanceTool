import sys
from PyQt5.QtWidgets import QWidget, QPushButton,QLineEdit,QTextEdit,QApplication,QToolTip

# class Example(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.initUI()
#
#     def initUI(self):
#         self.te = QTextEdit(self)
#         self.te.setToolTip('点击提交开始读取文件')   #可用气泡提示
#         self.te.move(50,50)
#         # self.te.textChanged.connect(self.onChanged)
#         self.btn = QPushButton('提交',self)
#         self.btn.clicked.connect(self.onChanged)
#         self.btn.move(350,150)
#         self.setGeometry(300, 300, 500, 300)
#         self.setWindowTitle('文本框')
#         self.show()

    # def onChanged(self):
    #     print(self.te.toPlainText())

class read_txt(QWidget):
    '''程序要求：
    读取txt文件内容，并在界面上显示出来
    '''
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.a = QLineEdit(self)
        self.a.setPlaceholderText('请输入读取文件的路径地址')
        self.a.setGeometry(50,20,320,20)
        self.te = QTextEdit(self)
        self.te.setGeometry(50,80,450,500)
        #
        self.btn = QPushButton('确定',self)
        self.btn.clicked.connect(self.onChanged)
        self.btn.move(400,15)
        self.setGeometry(300, 300, 600, 600)
        self.setWindowTitle('文本框')
        self.show()

    def onChanged(self):
        addr = self.a.text()
        print(self.a.text())
        f = open(addr,'r',encoding='utf-8')
        info = f.read()
        self.te.setPlainText(info)
        f.close()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = read_txt()
    sys.exit(app.exec_())