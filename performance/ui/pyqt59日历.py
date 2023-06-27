from PyQt5.QtWidgets import QWidget, QCalendarWidget,QLabel, QApplication
import sys

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        cal = QCalendarWidget(self)   #创建日历对象
        cal.setGridVisible(True)      #设置是否有网格
        cal.clicked.connect(self.showDate)
        self.lbl = QLabel(self)
        self.lbl.move(80,250)
        date = cal.selectedDate()
        print(date)
        self.lbl.setText(date.toString())#获取选中的日期，然后把日期对象转成字符串，在标签里面显示出来
        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('日历')
        self.show()

    def showDate(self, date):
        self.lbl.setText(date.toString())
        print(date.toString())
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())