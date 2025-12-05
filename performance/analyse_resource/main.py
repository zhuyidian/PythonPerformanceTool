import multiprocessing
import sys

from analyse_resource.cpuinfo_manager import CpuinfoManager
from analyse_resource.image.analyse_resource_image import AnalyseResourceImage
from analyse_resource.meminfo_manager import MeminfoManager
from analyse_resource.process_manager import ProcessManager
from utils.adb_utils import check_adb_device
from utils.file_utils import create_dir
from ui.progress_window import show
from utils.device_utils import get_device_chip_for_adb, get_device_type_for_adb, get_device_model_for_adb
import time
import os
from multiprocessing import Process, Queue

from utils.adb_utils import check_adb_device

analyse_dir = ''  # 性能分析缓存一级目录
device_filename = 'device.txt'  # 平台资源文件
process_all_filename = 'process_all.txt'  # 所有进程缓存文件
# cpu
analyse_cpuinfo_image_dir = '' #性能分析缓存cpuinfo image二级目录
analyse_cpuinfo_filename = 'analyse_cpuinfo'  # 资源分析汇总文件analyse_cpuinfo.xlsx
top_cpuinfo_filename = 'top_cpuinfo.txt'  # top缓存文件
extract_cpuinfo_filename = 'extract_cpuinfo.txt'  # 资源分析文件
# mem
dumpsys_meminfo_filename = 'dumpsys_meminfo.txt'  # dumpsys缓存文件
extract_meminfo_filename = 'extract_meminfo.txt'  # 资源分析文件
analyse_meminfo_image_dir = '' #性能分析缓存meminfo image二级目录
analyse_meminfo_filename = 'analyse_meminfo'  # 资源分析汇总文件analyse_meminfo.xlsx
# target
analyse_target_dir = '' #性能分析target二级目录
extract_resource_filename = 'extract_resource.txt'  # 资源分析文件


def task_progress_window(queue,name,start_time,tol_time):
    print('%s sub process %s is running......' % (name, os.getpid()))

    cpuinfo_isdone, meminfo_isdone = False, False
    # progress
    show(tol_time)
    while cpuinfo_isdone == False or meminfo_isdone == False:
        value = queue.get(True)
        print('task process window get value: %s' % value)
        if value == 'task cpuinfo done':
            cpuinfo_isdone = True
        elif value == 'task meminfo done':
            meminfo_isdone = True

    print('%s sub process %s is done.' % (name, os.getpid()))

def task_cpuinfo(queue,name,start_time,tol_time,root_dir,sub_dir,target_keywords,target_dir):
    print('%s sub process %s is running......' % (name,os.getpid()))

    cpuinfo_manager = CpuinfoManager()

    # tol_time = int(input("请输入脚本执行时间(分钟)："))
    # start_time = time.time()
    while True:
        end_time = time.time()
        # if (end_time - start_time) / 60 >= tol_time:  # 分钟
        if end_time - start_time >= tol_time:  # 秒
            break

        time.sleep(1)
        cpuinfo_manager.get_cpuinfo_once(f'{root_dir}/{top_cpuinfo_filename}')

    # 分析并且写入到excel
    for bean in cpuinfo_manager.system_cpuinfo_list:
        print(f'system cpuinfo list: usr={bean.usr}, sys={bean.sys}, nic={bean.nic}, idle={bean.idle},'
              f'io={bean.io},irq={bean.irq},sirq={bean.sirq}')
    for bean in cpuinfo_manager.process_cpuinfo_list:
        print(f'process cpuinfo list: pid={bean.pid_set}, name={bean.name}, cpu_list={bean.cpu_list}')
    cpuinfo_manager.write_to_excel(f'{root_dir}/{analyse_cpuinfo_filename}',
                                   f'{root_dir}/{extract_cpuinfo_filename}',
                                   AnalyseResourceImage(sub_dir),
                                   target_keywords,
                                   target_dir,
                                   f'{target_dir}/{extract_resource_filename}')
    print('%s sub process %s is done.' % (name, os.getpid()))
    queue.put('task cpuinfo done')

def task_meminfo(queue,name,start_time,tol_time,root_dir,sub_dir,target_keywords,target_dir):
    print('%s sub process %s is running......' % (name, os.getpid()))

    meminfo_manager = MeminfoManager()
    # tol_time = int(input("请输入脚本执行时间(分钟)："))
    # start_time = time.time()
    while True:
        end_time = time.time()
        # if (end_time - start_time) / 60 >= tol_time:  # 分钟
        if end_time - start_time >= tol_time:  # 秒
            break

        time.sleep(1)
        meminfo_manager.get_meminfo_once(f'{root_dir}/{dumpsys_meminfo_filename}')

    # 分析并且写入到excel
    for bean in meminfo_manager.system_meminfo_list:
        print(
            f'system meminfo list: total_ram={bean.total_ram}, free_ram={bean.free_ram}, used_ram={bean.used_ram}, lost_ram={bean.lost_ram},'
            f'free={bean.free},used_pss={bean.used_pss},kernel={bean.kernel},buffers={bean.buffers},shmem={bean.shmem},'
            f',slab={bean.slab},total_swap={bean.total_swap},used_swap={bean.used_swap}')
    for bean in meminfo_manager.process_meminfo_list:
        print(f'process meminfo list: pid={bean.pid_set}, name={bean.name}, mem_list={bean.mem_list}')
    meminfo_manager.write_to_excel(f'{root_dir}/{analyse_meminfo_filename}',
                                   f'{root_dir}/{extract_meminfo_filename}',
                                   AnalyseResourceImage(sub_dir),
                                   target_keywords,
                                   target_dir,
                                   f'{target_dir}/{extract_resource_filename}')
    print('%s sub process %s is done.' % (name, os.getpid()))
    queue.put('task meminfo done')

if __name__ == "__main__":
    # 在此处添加，用于多进程打包
    multiprocessing.freeze_support()

    # 判断adb是否连接
    device = check_adb_device()
    if device==False:
        print(f'!!!!!!未连接adb设备!!!!!!')
        sys.exit()

    # 获取芯片-机芯-机型
    chip = get_device_chip_for_adb()
    type = get_device_type_for_adb()
    model = get_device_model_for_adb()
    print(f'chip:{chip} type:{type} model:{model}')

    # 输入目标进程包名
    target_keywords = input("输入目标进程关键字：")
    print(f'target_keywords:{target_keywords}')

    # 输入脚本运行时长
    tol_time = int(input("请输入资源抓取时间(秒)："))
    start_time = time.time()

    # 记录开始时间点
    start_time_str = time.strftime("%y_%m_%d-%H_%M_%S", time.localtime())

    file_name = chip+"-"+type+"-"+model+"-"+start_time_str
    print(f'file_name:{file_name}')

    # 每次执行创建一个时间节点目录
    analyse_dir = os.getcwd() + "/temp/" + file_name
    create_dir(analyse_dir)
    analyse_cpuinfo_image_dir = analyse_dir + '/cpuinfo_image'
    create_dir(analyse_cpuinfo_image_dir)
    analyse_meminfo_image_dir = analyse_dir + '/meminfo_image'
    create_dir(analyse_meminfo_image_dir)
    analyse_target_dir = analyse_dir + '/target'
    create_dir(analyse_target_dir)

    # 使用ps命令获取所有进程
    process_manager = ProcessManager()
    process_manager.get_process_all(f'{analyse_dir}/{process_all_filename}')

    # 这里可以使用多进程机制
    print('Parent process %s' % os.getpid())
    queue = Queue()
    p0 = Process(target=task_progress_window, args=(queue,'ProgressWindow', start_time, tol_time,))
    p0.start()
    p1 = Process(target=task_cpuinfo, args=(queue,'Cpuinfo',start_time,tol_time,analyse_dir,analyse_cpuinfo_image_dir,target_keywords,analyse_target_dir,))
    p1.start()
    p2 = Process(target=task_meminfo, args=(queue,'Meminfo',start_time,tol_time,analyse_dir,analyse_meminfo_image_dir,target_keywords,analyse_target_dir,))
    p2.start()

    p1.join()  # join()方法可以等待子进程结束后再继续往下运行，通常用于进程间的同步
    p2.join()
    p0.join()

    print('资源分析结束！')
