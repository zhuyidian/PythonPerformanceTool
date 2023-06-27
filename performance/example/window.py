from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtGui import QIcon
import sys

"""
app = QApplication(sys.argv)  #sys.argv是一组命令行参数的列表，是一个从程序外部获取参数的桥梁
w = QWidget()  #QWidget控件是一个用户界面的基本控件，这里是一个窗口
w.resize(550,250)  #窗口的宽高
w.move(900,300)  #控件位置
w.setWindowTitle('test window')  #窗口标题
w.setWindowIcon(QIcon('python.png'))  #窗口标题前面的图标
w.show()  #show能让控件在桌面上显示出来
sys.exit(app.exec_())
"""

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initui()
    def initui(self):
        self.resize(350,350)
        self.move(900, 300)
        self.setWindowTitle('test window')
        self.setWindowIcon(QIcon('python.png'))
        self.show()

print('main外面执行')
"""
if __name__ == '__main__':的两种使用功能：
情况1、直接执行本py代码文件时，把包含的代码块视为脚本代码顺序执行
情况2、当本py代码文件作为其他代码import对象时，不执行如下被包含的代码
"""
if __name__ == '__main__':
    print('main里面执行')
    """
    QApplication管理GUI程序的控制流和主要设置 
    """
    """
    sys库作用：查看python解释器信息及传递信息给python解释器
    sys.argv：获取命令行参数列表，第一个元素是程序本身。从程序外部获取参数的桥梁，获取命令行参数，返回一个列表。\
    其中包含了脚本路径及传递给python脚本的命令行参数.并非等用户输入，可以由系统传递给python脚本程序。\
    优点是方便程序员可以通过命令方式直接控制程序的运行状态，不需要使用input对数据进行处理。
    sys.exit(n)：退出python程序，exit(0)表示正常退出，当参数非0时表示异常退出。
    sys.version：获取python解释器的版本信息
    """
    print(sys.argv)
    app = QApplication(sys.argv)
    ex = Example()
    print(app.exec_())  #0
    sys.exit(app.exec_())