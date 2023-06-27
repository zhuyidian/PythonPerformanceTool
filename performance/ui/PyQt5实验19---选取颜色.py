from PyQt5.QtWidgets import QWidget,QApplication,QPushButton,QFrame,QColorDialog
from PyQt5.QtGui import QColor
import  sys


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        col = QColor(100,100,0)
        self.btn = QPushButton("按钮",self)
        self.btn.move(20,20)
        self.btn.clicked.connect(self.showDialog)
        self.frm = QFrame(self)
        self.frm.setStyleSheet("QWidget { background-color: %s }"
            % col.name())
        self.frm.setGeometry(100,100,150,50)
        self.setGeometry(300,300,300,300)
        self.show()
    def showDialog(self):
        col = QColorDialog().getColor()
        if col.isValid():
            self.frm.setStyleSheet("QWidget { background-color: %s }"
            % col.name())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Example()
    sys.exit(app.exec_())