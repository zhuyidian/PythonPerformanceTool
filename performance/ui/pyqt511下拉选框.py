from PyQt5.QtWidgets import QWidget, QLabel, QComboBox, QApplication
import sys

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.lbl = QLabel("请选择班级", self)
        self.lbl.move(20, 50)
        combo = QComboBox(self)
        combo.addItem("一年级")
        combo.addItem("二年级")
        combo.addItem("三年级")
        combo.addItem("四年级")
        combo.addItem("五年级")
        combo.move(100, 50)

        combo.activated[str].connect(self.onActivated)
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('下拉选框')
        self.show()

    def onActivated(self, text):
        self.lbl.setText(text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())