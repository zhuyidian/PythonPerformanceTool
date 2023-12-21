from PyQt5.QtWidgets import QWidget, QCheckBox, QApplication
from PyQt5.QtCore import Qt
import sys

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.cb = QCheckBox('是否打印', self)
        self.cb.move(20, 20)
        # self.cb.toggle()
        self.cb.stateChanged.connect(self.savelist)

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('复选框')
        self.show()

    def savelist(self):
        print(self.cb.text())
        print( self.cb.checkState())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())