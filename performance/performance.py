import os
import shutil

import adb_test
import time
import csv
from matplotlib import pyplot as plt

from utils.resource_utils import get_current_package_for_adb

start_time_str = "" # 脚本开始执行时间
time_list = []  # 测量时间点，画图用

adb_cpu_filename = "performance/adb_cpuinfo.csv"  # 保存每次获取的系统cpu信息
adb_current_packagename_filename = "performance/adb_current_packagename.csv"  # 保存当前前台应用信息
performance_filename = "performance/performance-xxx.csv"  #保存performance相关信息
performance_collect_filename = "performance/performance_collect-xxx.csv"  #保存performance汇总关信息
performance_child_dir = "performance/xxx/" # performance子目录

"""
系统各类型CPU占用数据缓存
源数据：CPU:  0.0% usr  2.3% sys  0.0% nic 97.6% idle  0.0% io  0.0% irq  0.0% sirq
"""
system_usrcpu_list,system_syscpu_list,system_niccpu_list,system_idlecpu_list,system_iocpu_list,\
    system_irqcpu_list,system_sirqcpu_list = [],[],[],[],[],[],[]
"""
系统各类型CPU汇总数据缓存
"""
system_usrcpu_collect_list,system_syscpu_collect_list,system_niccpu_collect_list,system_idlecpu_collect_list,\
    system_iocpu_collect_list,system_irqcpu_collect_list,system_sirqcpu_collect_list = [],[],[],[],[],[],[]

process_cpu_list = []  # 进程CPU占用数据缓存
process_cpu_collect_list = []  # 进程CPU汇总数据缓存
package_name = []  # 当前前台应用全包名
app_list = [] #当前前台应用截取前15字符长度的包名

"""
----------------------------------公共方法区---------------------------------------------
"""
"""
提取系统各类型CPU使用
"""
def extract_system_cpuinfo(line,type):
    cpu_1 = line.split(type)[0]
    cpu_2 = cpu_1.split(' ')
    cpu = cpu_2[len(cpu_2) - 2]
    return cpu

"""
删除目录及文件
"""
def delete_dir_or_file(path_name):
    try:
        # os.rmdir(path_name)
        shutil.rmtree(path_name)
    except OSError as e:
        print("Error: %s : %s" % (path_name, e.strerror))

"""
创建目录
"""
def create_dir_or_file(path_name):
    os.makedirs(path_name)

"""
----------------------------------逻辑方法区---------------------------------------------
"""
# 获取当前前台应用
def get_current_appname_for_adb():
    global adb_current_packagename_filename
    name = ""
    adb_info = adb_test.shell("dumpsys window | grep mCurrentFocus")
    out, err = adb_info.communicate()
    out_info = out.decode('unicode-escape')
    with open(adb_current_packagename_filename, 'w', encoding='utf-8') as f:
        f.write(out_info)
    with open(adb_current_packagename_filename, encoding='utf-8', mode='r') as f:
        lines = f.readlines()
        for line in lines:
            if 'mCurrentFocus' in line:
                name1 = line.split('/')[0].split(' ')
                name = name1[len(name1) - 1]
    with open('performance/director.txt', encoding='utf-8', mode='w') as f_name:
        text = name
        f_name.write(text)
    print(f"当前前台运行的包名为: {text}")
    adb_ps = adb_test.shell("ps | grep com.tianci.movie  | awk '{ print $2 }'")
    out, err = adb_ps.communicate()
    ps_info = out.decode('unicode-escape')
    print(f"当前前台运行的pid为: {ps_info}")

# 获取当前前台进程简化名称（包名）
# 数据结构: package_name，app_list
def get_current_applist_for_file():
    global package_name,app_list
    lines = []
    with open('performance/director.txt', encoding='utf-8', mode='r') as f:
        lines_all = f.readlines()
        for appname in lines_all:
            package_name1 = appname
            appname_new = appname[0:15]
            package_name.append(package_name1)
            lines.append(appname_new)
        for line in lines:
            app_list.append(line.strip())
    print(f'前台运行完整包名列表package_name: {package_name}')
    print(f'前台运行精简包名列表app_list: {app_list}')

# csv头部
# 数据结构: performance_filename
def write_performance_cvs_head_to_file():
    global performance_filename

    headers = []
    headers.append('usr_cpu')
    headers.append('sys_cpu')
    headers.append('nic_cpu')
    headers.append('idle_cpu')
    headers.append('io_cpu')
    headers.append('irq_cpu')
    headers.append('sirq_cpu')
    headers.append('process_name')
    headers.append('process_cpu')
    with open(performance_filename, 'w+', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()

# csv头部
# 数据结构: performance_filename
def write_performance_collect_cvs_head_to_file():
    global performance_collect_filename

    headers = []
    headers.append('usr_cpu_min')
    headers.append('usr_cpu_max')
    headers.append('usr_cpu_average')

    headers.append('sys_cpu_min')
    headers.append('sys_cpu_max')
    headers.append('sys_cpu_average')

    headers.append('nic_cpu_min')
    headers.append('nic_cpu_max')
    headers.append('nic_cpu_average')

    headers.append('idle_cpu_min')
    headers.append('idle_cpu_max')
    headers.append('idle_cpu_average')

    headers.append('io_cpu_min')
    headers.append('io_cpu_max')
    headers.append('io_cpu_average')

    headers.append('irq_cpu_min')
    headers.append('irq_cpu_max')
    headers.append('irq_cpu_average')

    headers.append('sirq_cpu_min')
    headers.append('sirq_cpu_max')
    headers.append('sirq_cpu_average')

    headers.append('process_name')
    headers.append('process_cpu_min')
    headers.append('process_cpu_max')
    headers.append('process_cpu_average')
    with open(performance_collect_filename, 'w+', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()

# 获取top cpu info
def get_cpuinfo_for_adb():
    global adb_cpu_filename
    #adb_info = adb_test.shell("top -n 1")
    adb_info = adb_test.shell("busybox top -n 1")
    out, err = adb_info.communicate()
    out_info = out.decode('unicode-escape')
    with open(adb_cpu_filename, 'w+', encoding='utf-8') as f:
        f.write(out_info)

# 计算cpu数值
# 处理busybox top -n 1
"""
def do_calculate_cpu():
    global adb_cpu_filename
    with open(adb_cpu_filename, encoding="utf-8", mode="r") as f:
        lines = f.readlines()
        for appname in app_list:
            for lis in lines:
                # 适配低版本手机
                if appname in lis and '%' in lis:
                    now = time.strftime("%H:%M:%S", time.localtime())
                    time_list.append(now)
                    cpu_1 = lis.split('%')[0]
                    cpu_2 = cpu_1.split(' ')
                    # print(cpu_2)
                    cpu = cpu_2[len(cpu_2) - 1]
                    print(cpu, now)
                    cpu_list.append(cpu)
                    break
                # 适配高版本手机
                elif appname in lis:
                    now = time.strftime("%H:%M:%S", time.localtime())
                    time_list.append(now)
                    cpu1 = lis.split(' ')
                    # print(cpu1)
                    cpu2 = list(set(cpu1))
                    cpu2.sort(key=cpu1.index)
                    cpu_h = cpu2[len(cpu2) - 4]
                    print(cpu_h, now)
                    cpu_list.append(cpu_h)
                    break
                else:
                    pass
    print(f'calculate cpu cpu_list: {cpu_list}')
"""

# 计算cpu数值
# 处理top -n 1
def do_calculate_cpu():
    global adb_cpu_filename
    global system_usrcpu_list,system_syscpu_list,system_niccpu_list,system_idlecpu_list,system_iocpu_list,\
    system_irqcpu_list,system_sirqcpu_list
    global process_cpu_list,time_list
    with open(adb_cpu_filename, encoding="utf-8", mode="r") as f:
        lines = f.readlines()
        for appname in app_list:
            for lis in lines:
                if 'CPU' in lis and 'idle' in lis:  # 系统CPU
                    now = time.strftime("%H:%M:%S", time.localtime())
                    time_list.append(now)
                    # print(f'calculate system CPU: {lis}')
                    usr_cpu = extract_system_cpuinfo(lis, 'usr')
                    system_usrcpu_list.append(usr_cpu)
                    sys_cpu = extract_system_cpuinfo(lis, 'sys')
                    system_syscpu_list.append(sys_cpu)
                    nic_cpu = extract_system_cpuinfo(lis, 'nic')
                    system_niccpu_list.append(nic_cpu)
                    idle_cpu = extract_system_cpuinfo(lis, 'idle')
                    system_idlecpu_list.append(idle_cpu)
                    io_cpu = extract_system_cpuinfo(lis, 'io')
                    system_iocpu_list.append(io_cpu)
                    irq_cpu = extract_system_cpuinfo(lis, 'irq')
                    system_irqcpu_list.append(irq_cpu)
                    sirq_cpu = extract_system_cpuinfo(lis, 'sirq')
                    system_sirqcpu_list.append(sirq_cpu)
                    # print(f'calculate system CPU: usr_cpu={usr_cpu},sys_cpu={sys_cpu},nic_cpu={nic_cpu},'
                    #       f'idle_cpu={idle_cpu},io_cpu={io_cpu},irq_cpu={irq_cpu},sirq_cpu={sirq_cpu}')
                elif appname in lis:  # 计算应用的CPU
                    cpu1 = lis.split(' ')
                    cpu = cpu1[len(cpu1) - 2]
                    # print(cpu, now)
                    process_cpu_list.append(cpu)
                    break
                else:
                    pass
    print(f'calculate cpu: time_list={time_list}')
    print(f'calculate cpu: system_usrcpu_list={system_usrcpu_list}')
    print(f'calculate cpu: system_syscpu_list={system_syscpu_list}')
    print(f'calculate cpu: system_niccpu_list={system_niccpu_list}')
    print(f'calculate cpu: system_idlecpu_list={system_idlecpu_list}')
    print(f'calculate cpu: system_iocpu_list={system_iocpu_list}')
    print(f'calculate cpu: system_irqcpu_list={system_irqcpu_list}')
    print(f'calculate cpu: system_sirqcpu_list={system_sirqcpu_list}')
    print(f'calculate cpu: process_cpu_list={process_cpu_list}')

# 计算cpu汇总数值
def do_calculate_cpu_collect(type,highs_float):
    print(f"type：{type}")
    # 输出最低值和最高值
    highs_hl = sorted(highs_float)
    low_value = highs_hl[0]
    print(f"CPU最低值：{low_value}")
    high_value = highs_hl[len(highs_hl) - 1]
    print(f"CPU最高值：{high_value}")
    # 输出平均值
    total = 0
    for value in highs_float:
        total += value
    average_value = round(total / len(highs_float), 2)
    print(f"CPU平均值：{average_value}")
    if type == 'usr_cpu':
        system_usrcpu_collect_list.append(low_value)
        system_usrcpu_collect_list.append(high_value)
        system_usrcpu_collect_list.append(average_value)
        print(f'system_usrcpu_collect_list:{system_usrcpu_collect_list}')
    elif type == 'sys_cpu':
        system_syscpu_collect_list.append(low_value)
        system_syscpu_collect_list.append(high_value)
        system_syscpu_collect_list.append(average_value)
        print(f'system_syscpu_collect_list:{system_syscpu_collect_list}')
    elif type == 'nic_cpu':
        system_niccpu_collect_list.append(low_value)
        system_niccpu_collect_list.append(high_value)
        system_niccpu_collect_list.append(average_value)
        print(f'system_niccpu_collect_list:{system_niccpu_collect_list}')
    elif type == 'idle_cpu':
        system_idlecpu_collect_list.append(low_value)
        system_idlecpu_collect_list.append(high_value)
        system_idlecpu_collect_list.append(average_value)
        print(f'system_idlecpu_collect_list:{system_idlecpu_collect_list}')
    elif type == 'io_cpu':
        system_iocpu_collect_list.append(low_value)
        system_iocpu_collect_list.append(high_value)
        system_iocpu_collect_list.append(average_value)
        print(f'system_iocpu_collect_list:{system_iocpu_collect_list}')
    elif type == 'irq_cpu':
        system_irqcpu_collect_list.append(low_value)
        system_irqcpu_collect_list.append(high_value)
        system_irqcpu_collect_list.append(average_value)
        print(f'system_irqcpu_collect_list:{system_irqcpu_collect_list}')
    elif type == 'sirq_cpu':
        system_sirqcpu_collect_list.append(low_value)
        system_sirqcpu_collect_list.append(high_value)
        system_sirqcpu_collect_list.append(average_value)
        print(f'system_sirqcpu_collect_list:{system_sirqcpu_collect_list}')
    else:
        process_cpu_collect_list.append(type)
        process_cpu_collect_list.append(low_value)
        process_cpu_collect_list.append(high_value)
        process_cpu_collect_list.append(average_value)
        print(f'process_cpu_collect_list:{process_cpu_collect_list}')

# 控制监测时间
def exe_process_time_control():
    while True:
        end_time = time.time()
        #if (end_time - start_time) / 60 >= tol_time:  # 分钟
        if end_time - start_time >= tol_time:  # 秒
            break

        time.sleep(1)
        get_cpuinfo_for_adb()
        do_calculate_cpu()

# 将数值写入csv，用于绘图时读取
def write_performance_cvs_cpuinfo_to_file():
    global performance_filename
    # headers = ['name', 'aaa', 'init_cpu']
    with open(performance_filename, 'a+', newline='') as csvfile:
        writer = csv.writer(csvfile)
        if len(system_usrcpu_list)==len(system_syscpu_list)==len(system_niccpu_list)==len(system_idlecpu_list)==\
            len(system_iocpu_list)==len(system_irqcpu_list)==len(system_sirqcpu_list):
            print('system cpu info is OK')
        else:
            print('system cpu info is ERROR')
        for i in range(0,len(system_usrcpu_list)):
            writer.writerow([system_usrcpu_list[i], system_syscpu_list[i], system_niccpu_list[i], system_idlecpu_list[i],\
                          system_iocpu_list[i],system_irqcpu_list[i],system_sirqcpu_list[i],app_list[0],process_cpu_list[i]])
        # for key in process_cpu_list:
        #     writer.writerow([' ', key])

# 将数值写入csv，用于汇总
def write_performance_collect_cvs_cpuinfo_to_file():
    global performance_collect_filename
    with open(performance_collect_filename, 'a+', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([system_usrcpu_collect_list[0], system_usrcpu_collect_list[1], system_usrcpu_collect_list[2],\
                         system_syscpu_collect_list[0], system_syscpu_collect_list[1], system_syscpu_collect_list[2],\
                         system_niccpu_collect_list[0], system_niccpu_collect_list[1], system_niccpu_collect_list[2],\
                         system_idlecpu_collect_list[0], system_idlecpu_collect_list[1], system_idlecpu_collect_list[2],\
                         system_iocpu_collect_list[0], system_iocpu_collect_list[1], system_iocpu_collect_list[2],\
                         system_irqcpu_collect_list[0], system_irqcpu_collect_list[1], system_irqcpu_collect_list[2],\
                         system_sirqcpu_collect_list[0], system_sirqcpu_collect_list[1], system_sirqcpu_collect_list[2],\
                         process_cpu_collect_list[0], process_cpu_collect_list[1], process_cpu_collect_list[2],process_cpu_collect_list[3]])

# 绘制折线图，生成测试报告
# def do_mapping():
#     global performance_filename
#     with open(performance_filename) as f:
#         reader = csv.reader(f)
#         header_row = next(reader)
#         print(f'header_row={header_row}')
#         highs = []
#         for row in reader:
#             print(f'row={row}')
#             process_name = row[7]
#             high = row[8]
#             highs.append(high)
#     wights = time_list
#     highs_float = list(map(float, highs))
#     print(f"CPU值：{highs_float}")
#     # 输出平均值
#     total = 0
#     for value in highs_float:
#         total += value
#     average = round(total / len(highs_float), 2)
#     print(f"CPU平均值：{average}")
#
#     # 输出最低值和最高值
#     highs_hl = sorted(highs_float)
#     print(f"CPU最低值：{highs_hl[0]}")
#     print(f"CPU最高值：{highs_hl[len(highs_hl) - 1]}")
#
#     # 根据数据绘制图形
#     plt.figure(figsize=(11, 4), dpi=600)
#     # 生成网格
#     # plt.grid()
#     plt.grid(axis="y")
#     # 折线图
#     if package_name[0] == 'com.oneapp.max.security.pro.cn':
#         plt.plot(wights, highs_float, "c-", linewidth=1, label="PPP")
#     elif package_name[0] == 'com.oneapp.max.cn':
#         plt.plot(wights, highs_float, "c-", linewidth=1, label="Opt1.6.1")
#     elif package_name[0] == 'com.boost.clean.coin.cn':
#         plt.plot(wights, highs_float, "c-", linewidth=1, label="Fastclear")
#     elif package_name[0] == 'com.walk.sports.cn':
#         plt.plot(wights, highs_float, "c-", linewidth=1, label="Walk")
#     elif package_name[0] == 'com.diamond.coin.cn':
#         plt.plot(wights, highs_float, "c-", linewidth=1, label="Amber")
#     elif package_name[0] == 'com.oneapp.max.cleaner.booster.cn':
#         plt.plot(wights, highs_float, "c-", linewidth=1, label="Space")
#     else:
#         plt.plot(wights, highs_float, "c-", linewidth=1, label=package_name[0])
#     # 坐标轴范围
#     # plt.ylim(300, 400)
#     # plt.xlim(0, 10)
#
#     plt.xlabel('time(H:Min:S)', fontsize=16)
#     plt.ylabel("cpu_realtime(%)", fontsize=16)
#     plt.title("cpu real time line chart", fontsize=24)
#     plt.legend()
#
#     # 横坐标显示间隔
#     if len(wights) <= 15:
#         pass
#     else:
#         t = int(len(wights) / 15)
#         plt.xticks(range(0, len(wights), t))
#
#     # 纵坐标显示间隔
#     # plt.yticks(range(100, 300, 10))
#
#     # 旋转日期
#     plt.gcf().autofmt_xdate()
#
#     # 展示每个坐标
#     # for a, b in zip(wights, highs_float):
#     #     plt.text(a, b, (a, b), ha='center', va='bottom', fontsize=8)
#
#     # plt.show()
#
#     time_now = time.strftime("%y_%m_%d-%H_%M_%S", time.localtime())
#     path = performance_child_dir + process_name + ".jpg"
#     print(f"path: {path}")
#     plt.savefig(path)

# 绘制折线图，生成测试报告
def do_mapping():
    global performance_filename
    with open(performance_filename) as f:
        reader = csv.reader(f)
        header_row = next(reader)
        reader_list = list(reader)
        wights = time_list
        for i in range(len(header_row)):
            row_name = header_row[i]
            print(f"mapping: i={i},row_name={row_name}")
            highs = []
            highs_float = []
            if(row_name=='process_name'):
                continue
            for row in reader_list:
                print(f'row={row}')
                if row_name=='process_cpu':
                    row_name = row[i-1]
                high = row[i]
                highs.append(high.strip('%'))
            highs_float = list(map(float, highs))
            print(f"CPU值：{highs_float}")
            do_calculate_cpu_collect(row_name,highs_float)
            # # 输出最低值和最高值
            # highs_hl = sorted(highs_float)
            # print(f"CPU最低值：{highs_hl[0]}")
            # system_usrcpu_collect_list.append(highs_hl[0])
            # print(f"CPU最高值：{highs_hl[len(highs_hl) - 1]}")
            # system_usrcpu_collect_list.append(highs_hl[len(highs_hl) - 1])
            # # 输出平均值
            # total = 0
            # for value in highs_float:
            #     total += value
            # average = round(total / len(highs_float), 2)
            # print(f"CPU平均值：{average}")
            # system_usrcpu_collect_list.append(average)
            # 根据数据绘制图形
            plt.figure(figsize=(11, 4), dpi=600)
            # 生成网格
            # plt.grid()
            plt.grid(axis="y")
            # 折线图
            if package_name[0] == 'com.oneapp.max.security.pro.cn':
                plt.plot(wights, highs_float, "c-", linewidth=1, label="PPP")
            elif package_name[0] == 'com.oneapp.max.cn':
                plt.plot(wights, highs_float, "c-", linewidth=1, label="Opt1.6.1")
            elif package_name[0] == 'com.boost.clean.coin.cn':
                plt.plot(wights, highs_float, "c-", linewidth=1, label="Fastclear")
            elif package_name[0] == 'com.walk.sports.cn':
                plt.plot(wights, highs_float, "c-", linewidth=1, label="Walk")
            elif package_name[0] == 'com.diamond.coin.cn':
                plt.plot(wights, highs_float, "c-", linewidth=1, label="Amber")
            elif package_name[0] == 'com.oneapp.max.cleaner.booster.cn':
                plt.plot(wights, highs_float, "c-", linewidth=1, label="Space")
            else:
                plt.plot(wights, highs_float, "c-", linewidth=1, label=row_name)
            plt.xlabel('time(H:Min:S)', fontsize=16)
            plt.ylabel("cpu_realtime(%)", fontsize=16)
            plt.title("cpu real time line chart", fontsize=24)
            plt.legend()
            # 横坐标显示间隔
            if len(wights) <= 15:
                pass
            else:
                t = int(len(wights) / 15)
                plt.xticks(range(0, len(wights), t))
            # 旋转日期
            plt.gcf().autofmt_xdate()
            path = performance_child_dir + row_name + ".jpg"
            print(f"path: {path}")
            plt.savefig(path)

if __name__ == "__main__":
    delete_dir_or_file('performance/')
    start_time_str = time.strftime("%y_%m_%d-%H_%M_%S", time.localtime())
    performance_filename = "performance/" + "performance-" + start_time_str + ".csv"
    performance_collect_filename = "performance/" + "performance_collect-" + start_time_str + ".csv"
    performance_child_dir = "performance/" + start_time_str + "/"
    create_dir_or_file(performance_child_dir)

    get_current_appname_for_adb()
    pid,package_name = get_current_package_for_adb()

    get_current_applist_for_file()
    write_performance_cvs_head_to_file()
    write_performance_collect_cvs_head_to_file()

    tol_time = int(input("请输入脚本执行时间(分钟)："))
    start_time = time.time()

    # 设定时间内的CPU信息
    # exe_process_time_control()
    #
    # write_performance_cvs_cpuinfo_to_file()
    # do_mapping()
    # write_performance_collect_cvs_cpuinfo_to_file()