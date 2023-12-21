#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import platform
import re
import subprocess
import threading
import time
import tkinter as tk
import datetime
from tkinter import ttk
from typing import Union, Optional
from uiautomator2 import Device
import xml.etree.ElementTree as ET

from autoTestScripts.python.scriptUtils import exception, serial_util, file_utils

serial_num = ""

# 判断是否设置环境变量ANDROID_HOME
command = ""


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
            print(f"adb path:{command}")
            return

    if system == "Windows":
        user_name = os.environ['USERNAME']
        command = os.path.join(f"C:\\Users\\{user_name}\\AppData\\Local\\Android\\Sdk", "platform-tools", "adb.exe")
    if os.path.exists(command):
        command = f'"{command}"'  # 防止adb路径有空格
        print(f"adb path:{command}")
    else:
        raise EnvironmentError(
            "Adb not found in $ANDROID_HOME path: %s." % os.environ["ANDROID_HOME"])

def get_screen_size(window):
    return window.winfo_screenwidth(), window.winfo_screenheight()

def get_window_size(window):
    return window.winfo_reqwidth(), window.winfo_reqheight()

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
        logger.debug("show_window")
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
        logger.info(f"self.device_name_dict:{self.device_name_dict}")
        for key, value in self.device_name_dict.items():
            if value == self.box.selection_get():
                self.device_id = key
        # self.device_id = self.box.selection_get()

    def ok(self):
        global serial_num
        serial_num = self.device_id
        logger.info(f"you select serial_num:{serial_num}")
        self.root.destroy()

    def get_device_name_list(self):
        for id in self.device_id_list:
            self.device_name_list.append(self.device_name_dict.get(id))


def get_serial_num(_id=""):
    get_adb_path()
    global serial_num
    serial_num = _id
    if serial_num == "":
        devices = get_device_list()
        if len(devices) == 1:
            serial_num = devices[0]
        elif len(devices) > 1:
            root = tk.Tk()
            window = Window(devices, root)
            window.show_window()
    # 连接设备
    # adb("kill-server").wait()
    # adb("start-server").wait()
    __adb_without_num("wait-for-device").wait()
    # os.popen("adb -s %s get-state" % serial_num).read().strip()
    if adb("get-state").stdout.read().decode().strip() != "device":
        # adb("kill-server").wait()
        # adb("start-server").wait()
        raise exception.ScriptException("adb device not run")
    file_utils.auto_install_app()  # 在连接串口前安装好软件，因为串口检查优先使用性能监测软件执行特权命令
    serial_util.check_device_comport_state()  # 检查串口情况，以方便执行某些特权命令
    return serial_num


# adb命令
def adb(args):
    """用communicate或者wait等待命令执行成功"""
    global serial_num
    if serial_num == "":
        devices = get_device_list()
        if len(devices) == 1:
            serial_num = devices[0]
        elif len(devices) > 1:
            root = tk.Tk()
            window = Window(devices, root)
            window.show_window()
    cmd = "%s -s %s %s" % (command, serial_num, str(args))
    logger.debug(cmd)
    return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def __adb_without_num(args):
    """执行电脑端的adb命令，不是tv端，例如adb devices，用communicate或者wait等待命令执行成功"""
    cmd = "%s %s" % (command, str(args))
    logger.debug(cmd)
    return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


# adb shell命令
def shell(args):
    """用communicate或者wait等待命令执行成功"""
    global serial_num
    if serial_num == "":
        devices = get_device_list()
        if len(devices) == 1:
            serial_num = devices[0]
        elif len(devices) > 1:
            root = tk.Tk()
            window = Window(devices, root)
            window.show_window()
    # 给shell命令增加双引号，避免在Windows下面无法识别某些linux命令导致出错，uiautomator2自带adb工具无此问题
    cmd = '%s -s %s shell "%s"' % (command, serial_num, str(args))
    return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


# 获取设备上当前应用的包名与activity
def get_focused_package_and_activity():
    pattern = re.compile(r"[a-zA-Z0-9\.]+/.[a-zA-Z0-9\.]+")
    # tmp = shell("dumpsys activity | %s mFocusedActivity" %find_util).stdout.read()
    tmp = shell("dumpsys activity | grep mResumedActivity").stdout.read()
    tmp = tmp.decode()
    logger.debug("get_focused_package_and_activity命令执行结果:{}".format(tmp))
    name = ""
    names = pattern.findall(tmp)
    logger.debug("get_focused_package_and_activity:{}".format(names))
    if names.__len__() == 0:
        return ""
    try:
        name = names[0]
    except:
        tmp = shell("dumpsys window w | grep / | grep name=").stdout.read()
        tmp = tmp.decode()
        name = pattern.findall(tmp)[0]
    return name


# 获取当前焦点窗口的包名/类名或者service窗口
def get_focused_window():
    # mCurrentFocus=Window{18f714a u0 com.coocaa.os.ccosservice}
    # mCurrentFocus=Window{58a570 u0 com.coocaa.os.softsettings/com.coocaa.os.softsettings.framework.ui.SettingsActivity}
    pattern = re.compile(r"[a-zA-Z0-9\.]+/.[a-zA-Z0-9\.]+")
    tmp = shell("dumpsys window | grep -i mCurrentFocus").stdout.read().decode().replace('\n', '').replace('\r', '')
    logger.debug("get_focused_window命令执行结果:{}".format(tmp))
    names = pattern.findall(tmp)
    logger.debug("re.compile names:{}".format(names))
    if names.__len__() == 0:  # 如果是便捷面板，只会返回包名
        tmp_list = tmp.split()
        return tmp_list[-1].replace('}', '')
    return names[0]


def wait_activity(activity, timeout=10):
    """ wait activity
        Args:
            activity (str): name of activity
            timeout (float): max wait time

        Returns:
            bool of activity
        """
    deadline = time.time() + timeout
    while time.time() < deadline:
        current_activity = get_focused_window()
        if current_activity and activity in current_activity:
            return True
        time.sleep(.5)
    return False


def app_stop(package_name):
    """ Stop one application: am force-stop"""
    shell(f"am force-stop {package_name}").communicate()

def app_wait(
        package_name: str,
        timeout: float = 20.0,
        front=False) -> int:
    """ Wait until app launched
        Args:
            package_name (str): package name
            timeout (float): maxium wait time
            front (bool): wait until app is current app

        Returns:
            pid (int) 0 if launch failed
        """
    pid = None
    deadline = time.time() + timeout
    while time.time() < deadline:
        if front:
            current_activity = get_focused_window()
            if current_activity and package_name in current_activity:
                pid = get_pkg_pid(package_name)
                break
        else:
            pid = get_pkg_pid(package_name)
            if pid > 0:
                break
        time.sleep(1)

    return pid or 0


def app_start(d: Device, package_name: str, activity: Optional[str] = None, wait: bool = False, stop: bool = False,
              use_monkey: bool = False):
    """ Launch application
    Args:
        d: Device
        package_name (str): package name
        activity (str): app activity
        stop (bool): Stop app before starting the activity. (require activity)
        use_monkey (bool): use monkey command to start app when activity is not given
        wait (bool): wait until app started. default False
    """
    if stop:
        d.app_stop(package_name)

    if use_monkey:
        d.shell([
            'monkey', '-p', package_name, '-c',
            'android.intent.category.LAUNCHER', '1'
        ])
        if wait:
            app_wait(package_name)
        return

    if not activity:
        info = d.app_info(package_name)
        activity = info['mainActivity']
        if activity.find(".") == -1:
            activity = "." + activity

    # -D: enable debugging
    # -W: wait for launch to complete
    # -S: force stop the target app before starting the activity
    # --user <USER_ID> | current: Specify which user to run as; if not
    #    specified then run as the current user.
    # -e <EXTRA_KEY> <EXTRA_STRING_VALUE>
    # --ei <EXTRA_KEY> <EXTRA_INT_VALUE>
    # --ez <EXTRA_KEY> <EXTRA_BOOLEAN_VALUE>
    args = [
        'am', 'start', '-a', 'android.intent.action.MAIN', '-c',
        'android.intent.category.LAUNCHER',
        '-n', f'{package_name}/{activity}'
    ]
    d.shell(args)

    if wait:
        app_wait(package_name)


def get_input_device_path(device_default_name: str = "IR"):
    if device_default_name is None:
        device_default_name = "IR"
    device_path = ""
    for x in range(15):
        file = "/sys/class/input/event%d/device/name" % x
        result = shell('if [ -f "%s" ];then cat "%s"; else echo "no"; fi;' % (file, file)).stdout.read().decode()
        logger.debug("file %s,device_path:%s" % (file, result))
        m = re.search(device_default_name, result, re.IGNORECASE)
        if bool(m):
            device_path = "/dev/input/event%d" % x
            break

    logger.debug("device_path:%s" % device_path)
    return device_path


# 方便电视按键监测
def send_key_event(device_path: str, key: Union[int, str], long_press_flag: bool = False, press_time: float = 5):
    """
    press key via name or key code (linux not android). Supported key name includes:
    home, left, right, up, down, enter, select
    """
    key_dict = {'enter': 28, 'home': 102, 'up': 103, "left": 105, 'right': 106, 'down': 108, 'select': 353, 'menu': 139,
                'source': 466}
    if isinstance(key, int):
        key_code = key
    else:
        key_code = key_dict[key]
    logger.debug("send_key_event keycode: %d" % key_code)
    cmd_down = 'sendevent %s 1 %d 1' % (device_path, key_code)
    cmd2 = 'sendevent %s 0 0 0' % device_path
    cmd_up = 'sendevent %s 1 %d 0' % (device_path, key_code)
    if long_press_flag:
        deadline = time.time() + press_time
        shell(cmd_down + ' && ' + cmd2).wait()
        while time.time() <= deadline:
            pass
        shell(cmd_up + ' && ' + cmd2).wait()
    else:
        shell(cmd_down + ' && ' + cmd2 + " && " + cmd_up + " && " + cmd2).wait()


# 获取当前应用的包名
def get_current_package_name():
    return get_focused_package_and_activity().split("/")[0]


# 获取当前设备的activity
def get_current_activity():
    return get_focused_package_and_activity().split("/")[-1]


hierarchy_flag = False
hierarchy_num = 0
max_hierarchy = 0


def walk_data(root_node):
    global hierarchy_flag, hierarchy_num, max_hierarchy
    logger.debug(root_node.tag, root_node.attrib)
    if root_node.tag == "node":
        if hierarchy_flag:
            hierarchy_num += 1
            max_hierarchy = max(max_hierarchy, hierarchy_num)
        if root_node.attrib['resource-id'] == 'android:id/content':
            hierarchy_flag = True

    children_node = root_node.findall('node')
    for child in children_node:
        walk_data(child)

    if root_node.tag == "node":
        if hierarchy_flag:
            hierarchy_num -= 1
        if root_node.attrib['resource-id'] == 'android:id/content':
            hierarchy_flag = False
    return


def get_time(func):
    def inner(*arg, **kwarg):
        s_time = time.time()
        res = func(*arg, **kwarg)
        e_time = time.time()
        logger.info('{}耗时：{}秒'.format(func.__name__, e_time - s_time))
        return res

    return inner


@get_time
def get_view_tree_hierarchy(d: Device):
    global hierarchy_flag, hierarchy_num, max_hierarchy
    hierarchy_flag = False
    hierarchy_num = 0
    max_hierarchy = 0
    logger.debug('get_view_tree_hierarchy')
    xml = d.dump_hierarchy()
    root = ET.fromstring(xml)
    logger.debug('root_tag:', root.tag)
    logger.debug(xml)
    walk_data(root)
    logger.debug("view_max_hierarchy: %d" % max_hierarchy)
    return max_hierarchy


@get_time
def get_view_hierarchy_content(d: Device) -> str:
    return d.dump_hierarchy()


# 时间戳
def timestamp():
    return time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))


def time_to_seconds(_time: str):
    time2 = datetime.datetime.strptime(_time, "%Y-%m-%d %H:%M:%S")  # 2023-01-05 17:23:47
    time3 = time.mktime(time2.timetuple())
    # time4 = int(time3)
    logger.debug("{} to {}".format(_time, time3))
    return time3


def function_wait(timeout=30, count=0, target_reset=None, args_reset=(), target=None, args=()):
    start_time = time.time()
    deadline = start_time + timeout
    logger.info("function_wait start:{}".format(start_time))
    try:
        if target_reset is not None:
            target_reset(*args_reset)
    finally:
        pass
    if count > 0:
        for i in range(count):
            try:
                if target is not None:
                    target(*args)
            finally:
                pass
        logger.info("function_wait end :{}".format(time.time() - start_time))
        return
    while time.time() < deadline:
        try:
            if target is not None:
                target(*args)
        finally:
            pass

    logger.info("function_wait end :{}".format(time.time() - start_time))


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
    logger.info(result)
    for line in result[1:]:
        line = line.decode()
        if "attached" not in line.strip() and "offline" not in line.strip():
            devices.append(line.split()[0])
    if not devices:
        logger.error("没有发现adb设备")
    logger.info(f"devices:{devices}")
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
    return device_dict


def get_pkg_pid(pkg):
    try:
        app_pid = int(shell(f"busybox pidof {pkg}").stdout.read().decode().replace('\n', '').replace('\r', ''))
        logger.info(f"{pkg} pid is {app_pid}")
        return app_pid
    except ValueError:
        logger.error(f"{pkg} app is not alive")
        return -1


class WatchingPidThread(threading.Thread):
    def __init__(self, pkg, pid, func, args=()):
        threading.Thread.__init__(self, daemon=True)
        self.func = func
        self.args = args
        self.pkg = pkg
        self.pid = pid
        self.killed = False

    def kill(self):
        self.killed = True

    def run(self):
        while get_pkg_pid(self.pkg) == self.pid and not self.killed:
            logger.info(f"{self.pkg} is alive")
            time.sleep(10)
        if self.killed:
            logger.info("thread is killed")
            return
        self.func(*self.args)


apk_list = [
    # "com.tianci.movieplatform",
    # "com.tianci.appstore",
    # "com.coocaa.os.ccosservice",
    # "com.coocaa.playtvskill",
    # "com.coocaa.lifeassistant",
    # "com.coocaa.os.thememanager",
    # "com.tianci.de",
    # "com.coocaa.tvpi"
]


def disable_apks(white_list):
    # 进入到简易版主页再禁程序
    logger.info("disable_apks")
    shell("am start -n com.coocaa.simple.launcher/com.coocaa.simple.launcher.MainActivity").communicate()
    time.sleep(2)
    for i in apk_list:
        if i not in white_list:
            pm_command = "pm disable " + i
            logger.info(pm_command)
            serial_util.exec_command_by_serial(pm_command)
        else:
            logger.info(f"忽略{i}")


def enable_apks(white_list):
    for i in apk_list:
        if i not in white_list:
            pm_command = "pm enable " + i
            logger.info(pm_command)
            serial_util.exec_command_by_serial(pm_command)
        else:
            logger.info(f"忽略{i}")


if __name__ == "__main__":
    # logger.debug(get_focused_package_and_activity())
    # time_to_seconds("2023-01-05 17:23:47")
    # logger.debug(get_focused_window())
    get_serial_num()
