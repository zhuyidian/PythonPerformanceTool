import os
import platform
import subprocess
from tkinter import ttk
import tkinter as tk
import time
import uiautomator2 as u2

from utils.file_utils import get_project_root_path

device_once = "" # 连接的设备如：ip port
command = ""  # adb.exe的位置

"""
获取adb.exe的位置
"""
def get_adb_path():
    global command
    # 判断系统类型，windows使用findstr，linux使用grep
    system = platform.system()
    if "ANDROID_HOME" in os.environ:
        if system == "Windows":
            command = os.path.join(os.environ["ANDROID_HOME"], "platform-tools", "adb.exe")
        else:
            command = os.path.join(os.environ["ANDROID_HOME"], "platform-tools", "adb")
        if os.path.exists(command):
            command = f'"{command}"'  # 防止adb路径有空格
            print(f"adb path: command={command}")
            return

    if system == "Windows":
        user_name = os.environ['USERNAME']
        command = os.path.join(f"C:\\Users\\{user_name}\\AppData\\Local\\Android\\Sdk", "platform-tools", "adb.exe")
    if os.path.exists(command):
        command = f'"{command}"'  # 防止adb路径有空格
        print(f"adb path: command={command}")
    else:
        raise EnvironmentError(
            "Adb not found in $ANDROID_HOME path: %s." % os.environ["ANDROID_HOME"])

"""
执行adb device 命令
"""
def __adb_without_num(args):
    """执行电脑端的adb命令，不是tv端，例如adb devices，用communicate或者wait等待命令执行成功"""
    cmd = "%s %s" % (command, str(args))
    print(f'adb device cmd: {cmd}')
    return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

"""
获取具体设备
"""
def get_device_list():
    get_adb_path()
    devices = []
    p = __adb_without_num("devices")
    result = p.stdout.readlines()
    # stdout, stderr = p.communicate()
    # try:
    #     logger.info(f"stdout:{stdout.decode('utf-8')}")
    #     logger.error(f"stderr:{stderr.decode('utf-8')}")
    #     logger.error(f"stderr gbk:{stderr.decode('gbk')}")
    # except Exception as e:
    #     logger.error(e)
    result.reverse()
    # print(f'get device list: {result}')
    for line in result[1:]:
        line = line.decode()
        if "attached" not in line.strip() and "offline" not in line.strip():
            # print(f"发现adb设备: {line.split()[0]}")
            devices.append(line.split()[0])
    if not devices:
        print("没有发现adb设备")
    print(f"devices: {devices}")
    return devices

"""
获取设备名称
"""
def get_device_name_dict(devices):
    device_dict = {}
    if not devices:
        return device_dict

    for device in devices:
        cmd = "adb -s %s shell getprop ro.product.model" % device
        device_name = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE).stdout.readline().strip()
        device_dict[device] = device_name.decode("utf-8")
        # if not device_dict[device]:
        #     device_dict[device] = 'test'
    # print(f"device_dict: {device_dict}")
    return device_dict

"""
创建window
"""
def center_window(root, width, height):
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    root.geometry(size)

class Window(object):
    device_id = ""
    device_id_list = []
    device_name_list = []
    device_name_dict = {}
    root = None
    box = None

    def __init__(self, device_id_list, root):
        self.device_id_list = device_id_list
        self.device_name_dict = get_device_name_dict(self.device_id_list)
        self.get_device_name_list()
        self.device_id = device_id_list[0]
        self.root = root
        self.box = None

    def show_window(self):
        print("device choice show window")
        self.root.title(u'device choice')
        center_window(self.root, 300, 240)
        self.root.maxsize(600, 400)
        self.root.minsize(300, 240)

        # options = self.device_id_list
        options = self.device_name_list
        self.box = ttk.Combobox(values=options)
        self.box.current(0)
        self.box.pack(expand=tk.YES)
        self.box.bind("<<ComboboxSelected>>", self.select)
        ttk.Button(text=u"确定", command=self.ok).pack(expand=tk.YES)

        self.root.mainloop()

    def select(self, event=None):
        print(f"device dict:{self.device_name_dict}")
        for key, value in self.device_name_dict.items():
            if value == self.box.selection_get():
                self.device_id = key
        # self.device_id = self.box.selection_get()
        print(f"choice device id:{self.device_id}")

    def ok(self):
        global device_once
        device_once = self.device_id
        print(f"you choice device id:{device_once}")
        self.root.destroy()

    def get_device_name_list(self):
        for id in self.device_id_list:
            self.device_name_list.append(self.device_name_dict.get(id))

def check_adb_device():
    devices = get_device_list()
    if not devices:
        return False
    return True

# adb命令
def adb(args):
    """用communicate或者wait等待命令执行成功"""
    global device_once
    if device_once == "":
        devices = get_device_list()
        if len(devices) == 1:
            device_once = devices[0]
            # root = tk.Tk()
            # window = Window(devices, root)
            # window.show_window()
        elif len(devices) > 1:
            root = tk.Tk()
            window = Window(devices, root)
            window.show_window()
    cmd = "%s -s %s %s" % (command, device_once, str(args))
    print(f'adb cmd: {cmd}')
    return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# adb shell命令
def shell(args):
    """用communicate或者wait等待命令执行成功"""
    global device_once
    if device_once == "":
        devices = get_device_list()
        if len(devices) == 1:
            device_once = devices[0]
            # root = tk.Tk()
            # window = Window(devices, root)
            # window.show_window()
        elif len(devices) > 1:
            root = tk.Tk()
            window = Window(devices, root)
            window.show_window()
    # 给shell命令增加双引号，避免在Windows下面无法识别某些linux命令导致出错，uiautomator2自带adb工具无此问题
    cmd = '%s -s %s shell "%s"' % (command, device_once, str(args))
    print(f'adb shell cmd: {cmd}')
    return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

if __name__ == "__main__":
    """
    # 使用封装的adb执行adb shell命令
    # 方式一：
    top_info = shell("busybox top -n 1")
    out,err = top_info.communicate()
    out_info = out.decode('unicode-escape')  # 或者out_info = out.decode('utf-8')
    print(f'adb cmd: output={out_info}')
    # 方式二：
    top_info = shell("busybox top -n 1").stdout.readlines()
    # print(f'adb cmd: output={top_info}')
    print(f'adb cmd: ')
    for line in top_info:
        line = line.decode().replace('\n', '').replace('\r', '')
        print(f'{line}')
    # 方式三：
    top_info = shell("busybox top -n 1")
    # print(f'adb cmd: output={top_info}')
    print(f'adb cmd: ')
    while True:
        buff = top_info.stdout.readline().decode()
        print(f'{buff}')
        # 这个条件并不能正确判断
        if buff == '' and top_info.poll()!=None:
            break
    # 方式五：
    top_info = shell("busybox top -n 1").stdout.read().decode()
    print(f'adb cmd: output={top_info}')
    # 方式六：
    top_info = shell("busybox top -n 1").stdout.read().decode()
    info_list = str(top_info).strip().split('\r\n')[1:]
    for info in info_list:
        print(f'{info}')
    """

    """
    # 使用uiautomator2执行adb shell命令
    d = u2.connect()
    output, exit_code = d.shell("busybox top -n 1", timeout=60)
    print(f'uiautomator2 adb cmd: output={output}')
    """