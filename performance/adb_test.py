import os
import platform
import subprocess
from tkinter import ttk
import tkinter as tk
import time
import uiautomator2 as u2

serial_num = ""
command = ""  # 判断是否设置环境变量ANDROID_HOME

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

def __adb_without_num(args):
    """执行电脑端的adb命令，不是tv端，例如adb devices，用communicate或者wait等待命令执行成功"""
    cmd = "%s %s" % (command, str(args))
    print(f'cmd: {cmd}')
    return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

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
    print(f'get device list: {result}')
    for line in result[1:]:
        line = line.decode()
        if "attached" not in line.strip() and "offline" not in line.strip():
            devices.append(line.split()[0])
    if not devices:
        print("没有发现adb设备")
    print(f"devices: {devices}")
    return devices

def get_device_name_dict(devices):
    device_dict = {}
    if not devices:
        return device_dict

    for device in devices:
        cmd = "adb -s %s shell getprop ro.product.model" % device
        device_name = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE).stdout.readline().strip()
        device_dict[device] = device_name.decode("utf-8")
    print(f"device_dict: {device_dict}")
    return device_dict

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
        print("show window")
        self.root.title(u'Serialno Number')
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
        print(f"self.device_name_dict:{self.device_name_dict}")
        for key, value in self.device_name_dict.items():
            if value == self.box.selection_get():
                self.device_id = key
        # self.device_id = self.box.selection_get()

    def ok(self):
        global serial_num
        serial_num = self.device_id
        print(f"you select serial_num:{serial_num}")
        self.root.destroy()

    def get_device_name_list(self):
        for id in self.device_id_list:
            self.device_name_list.append(self.device_name_dict.get(id))

# adb命令
def adb(args):
    """用communicate或者wait等待命令执行成功"""
    global serial_num
    if serial_num == "":
        devices = get_device_list()
        if len(devices) == 1:
            serial_num = devices[0]
            root = tk.Tk()
            window = Window(devices, root)
            window.show_window()
        elif len(devices) > 1:
            root = tk.Tk()
            window = Window(devices, root)
            window.show_window()
    cmd = "%s -s %s %s" % (command, serial_num, str(args))
    print(f'adb: {cmd}')
    return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# adb shell命令
def shell(args):
    """用communicate或者wait等待命令执行成功"""
    global serial_num
    if serial_num == "":
        devices = get_device_list()
        if len(devices) == 1:
            serial_num = devices[0]
            root = tk.Tk()
            window = Window(devices, root)
            window.show_window()
        elif len(devices) > 1:
            root = tk.Tk()
            window = Window(devices, root)
            window.show_window()
    # 给shell命令增加双引号，避免在Windows下面无法识别某些linux命令导致出错，uiautomator2自带adb工具无此问题
    cmd = '%s -s %s shell "%s"' % (command, serial_num, str(args))
    print(f'cmd: {cmd}')
    return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

if __name__ == "__main__":
    # logger.debug(get_focused_package_and_activity())
    # time_to_seconds("2023-01-05 17:23:47")
    # logger.debug(get_focused_window())
    """
    serialNo = []
    resp = shell('dumpsys activity | grep mResumedActivity').stdout.read().decode()
    deviceInfo = str(resp).strip().split('\r\n')[1:]
    for info in deviceInfo:
        serialNo.append(info.split('\t')[0])
    print(serialNo)

    serialNo1 = []
    resp1 = shell("ll").stdout.read().decode()
    deviceInfo1 = str(resp1).strip().split('\r\n')[1:]
    for info in deviceInfo1:
        serialNo1.append(info.split('\t')[0])
    print(serialNo1)
    """
    """
    top_info = shell("top -n 1")
    print(top_info)
    out, err = top_info.communicate()
    out_info = out.decode('unicode-escape')
    print(out_info)
    lines = []
    lines = out_info.split('n')
    print(lines)
    """
    """
    time2sleep = 2.5
    while True:
        print (int(time.time())),
        #print (os.popen('top -bi -n 2 -d 0.02').read().split('\n\n\n')[1].split('\n')[1])
        print (os.popen('top -n 2 -d 0.02').read())
        time.sleep(time2sleep)
    """
    # top_info = shell("busybox top -n 1")
    # out,err = top_info.communicate()
    # out_info = out.decode('unicode-escape')
    # print(out_info)
    # with open('top.txt', 'w', encoding='utf-8') as f:
    #     f.write(out_info)
    # lines = []
    # lines = out_info.split('\n')
    # print(f'CPU: {lines[2]}')
    # with open('top.txt', 'w', encoding='utf-8') as f:
    #     f.write(lines[2])
    d = u2.connect()
    output, exit_code = d.shell("busybox top -n 1", timeout=60)
    print(f'u2: output={output}')