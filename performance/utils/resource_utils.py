import adb_test

"""
获取系统所有进程
"""
def get_process_all_for_adb():
    adb_info = adb_test.shell("ps")
    #out, err = adb_info.communicate()
    #out_info = out.decode('unicode-escape')
    return adb_info

"""
获取top信息
"""
def get_cpuinfo_for_adb():
    #adb_info = adb_test.shell("top -n 1")
    adb_info = adb_test.shell("busybox top -n 1")
    #out, err = adb_info.communicate()
    #out_info = out.decode('unicode-escape')
    return adb_info

"""
获取系统内存信息
"""
def get_meminfo_for_adb():
    adb_info = adb_test.shell("dumpsys meminfo")
    return adb_info

"""
获取当前运行进程的pid和包名
"""
# 获取当前前台应用
def get_current_package_for_adb():
    adb_info = adb_test.shell("dumpsys window | grep mCurrentFocus").stdout.readlines()
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
    adb_ps = adb_test.shell(f'ps | grep {package_name} | awk {awk_str}').stdout.read()
    package_ps = adb_ps.decode().replace('\n', '').replace('\r', '').strip()
    # print(f"当前运行的进程PID为: {package_ps}")
    return package_ps,package_name

"""
获取当前运行进程的pid和包名
"""
def get_current_appname_for_adb_1(path_name):
    package_name = ''
    package_ps = ''
    adb_info = adb_test.shell("dumpsys window | grep mCurrentFocus")
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
    adb_ps = adb_test.shell("ps | grep com.tianci.movie  | awk '{ print $2 }'")
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