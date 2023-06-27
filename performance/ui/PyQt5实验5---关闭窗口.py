from PyQt5.QtWidgets import QApplication,QWidget,QPushButton
from PyQt5.QtCore import QCoreApplication
import sys

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.resize(350, 150)
        ptn = QPushButton("退出",self)
        ptn.move(200,100)
        ptn.clicked.connect(QCoreApplication.instance().quit)
        self.setWindowTitle("自习室收费系统")
        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    a = Example()
    sys.exit(app.exec_())