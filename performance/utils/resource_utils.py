from utils import adb_utils
import os
import re

"""
获取系统所有进程
"""
def get_process_all_for_adb():
    adb_info = adb_utils.shell("ps")
    #out, err = adb_info.communicate()
    #out_info = out.decode('unicode-escape')
    return adb_info

"""
获取top信息
"""
def get_cpuinfo_for_adb():
    #adb_info = adb_test.shell("top -n 1")
    adb_info = adb_utils.shell("busybox top -n 1")
    #out, err = adb_info.communicate()
    #out_info = out.decode('unicode-escape')
    return adb_info

"""
获取系统内存信息
"""
def get_meminfo_for_adb():
    adb_info = adb_utils.shell("dumpsys meminfo")
    return adb_info

"""
获取当前运行进程的pid和包名
"""
# 获取当前前台应用
def get_current_package_for_adb():
    adb_info = adb_utils.shell("dumpsys window | grep mCurrentFocus").stdout.readlines()
    package_name = ''
    package_ps = ''
    for line_ in adb_info:
        if type(line_) is str:
            line = line_.replace('\n', '').replace('\r', '')
        else:
            line = line_.decode().replace('\n', '').replace('\r', '')
        if 'mCurrentFocus' in line:
            name1 = line.split('/')[0].split(' ')
            package_name = name1[len(name1) - 1]
            break
    # print(f"当前运行的进程包名为: {package_name}")
    awk_str = "'{ print $2 }'"
    adb_ps = adb_utils.shell(f'ps | grep {package_name} | awk {awk_str}').stdout.read()
    package_ps = adb_ps.decode().replace('\n', '').replace('\r', '').strip()
    # print(f"当前运行的进程PID为: {package_ps}")
    return package_ps,package_name

"""
获取当前运行进程的pid和包名
"""
def get_current_appname_for_adb_1(path_name):
    package_name = ''
    package_ps = ''
    adb_info = adb_utils.shell("dumpsys window | grep mCurrentFocus")
    out, err = adb_info.communicate()
    out_info = out.decode('unicode-escape')
    # out_info = out.decode('utf-8')
    # print('code:',adb_info.returncode)
    with open(path_name, 'w', encoding='utf-8') as f:
        f.write(out_info)
    with open(path_name, encoding='utf-8', mode='r') as f:
        lines = f.readlines()
        for line in lines:
            if 'mCurrentFocus' in line:
                name1 = line.split('/')[0].split(' ')
                package_name = name1[len(name1) - 1]
    # print(f"当前前台运行的包名为: {package_name}")
    adb_ps = adb_utils.shell("ps | grep com.tianci.movie  | awk '{ print $2 }'")
    out, err = adb_ps.communicate()
    package_ps = out.decode('unicode-escape')
    # print(f"当前前台运行的pid为: {package_ps}")
    return package_ps,package_name

"""
提取系统各类型CPU使用
"""
def extract_system_cpuinfo(line,type):
    cpu_1 = line.split(type)[0]
    cpu_2 = cpu_1.split(' ')
    cpu = cpu_2[len(cpu_2) - 2]
    return cpu

"""
push shell脚本文件到设备
"""
def push_shell_to_device(path):
    # path = get_project_root_path() + "/shell/fps_info.sh"
    print(f"push shell path: {path}")
    if not os.path.exists(path):
        print("push fps_info.sh is no find")
        return False
    adb_utils.adb("push " + path + " /data/local/tmp").wait()
    print("push fps_info.sh succeed.")
    return True

"""
获取sdk版本
"""
def get_sdk_version():
    adb_version = adb_utils.shell("getprop ro.build.version.sdk").stdout.read()
    version = adb_version.decode().replace('\n', '').replace('\r', '').strip()
    return version

"""
获取当前焦点窗口的包名/类名或者service窗口
"""
def get_focused_window():
    # mCurrentFocus=Window{18f714a u0 com.coocaa.os.ccosservice}
    # mCurrentFocus=Window{58a570 u0 com.coocaa.os.softsettings/com.coocaa.os.softsettings.framework.ui.SettingsActivity}
    pattern = re.compile(r"[a-zA-Z0-9\.]+/.[a-zA-Z0-9\.]+")
    tmp = adb_utils.shell("dumpsys window | grep -i mCurrentFocus").stdout.read().decode().replace('\n', '').replace('\r', '')
    print("get_focused_window命令执行结果:{}".format(tmp))
    names = pattern.findall(tmp)
    print("re.compile names:{}".format(names))
    if names.__len__() == 0:  # 如果是便捷面板，只会返回包名
        tmp_list = tmp.split()
        return tmp_list[-1].replace('}', '')
    return names[0]

