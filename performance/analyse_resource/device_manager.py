from analyse_resource.bean.process_cpuinfo_bean import ProcessCpuinfoBean
from analyse_resource.bean.system_cpuinfo_bean import SystemCpuinfoBean
from analyse_resource.excel.analyse_resource_excel import AnalyseResourceExcel
from analyse_resource.excel.analyse_resource_excel_data import AnalyseResourceExcelData
from analyse_resource.image.analyse_resource_image import AnalyseResourceImage
from analyse_resource.process_manager import ProcessManager
from utils import resource_utils
from utils import file_utils
from utils.analyse_data_utils import analyse_min_max_average, analyse_str_is_float, analyse_str_is_float_or_int
import time
import psutil
from utils.resource_utils import get_current_package_for_adb


class DeviceManager:
    def __init__(self,path_name):
        self.path_name = path_name
        self.device_info_list = []

    def getCpuinfo(self):
        # 结果为 6，说明是 6 核超线程；如果 CPU 的物理核心数 和 逻辑数相等，也为 12，则说明是 12 核非超线程。
        cpu_physical_num = psutil.cpu_count(logical=False)
        cpu_logic_num = psutil.cpu_count()
        print(f'CPU物理数量: {cpu_physical_num}, CPU逻辑数量: {cpu_logic_num}')
        self.device_info_list.append(f'CPU物理数量: {cpu_physical_num}')
        self.device_info_list.append(f'CPU逻辑数量: {cpu_logic_num}')

        cpu_freq = psutil.cpu_freq()
        print(f'CPU频率: {cpu_freq}')
        self.device_info_list.append(f'CPU频率: {cpu_freq}')

        cpu_stats = psutil.cpu_stats()
        print(f'CPU上下文切换/中断/软中断/系统调用次数: {cpu_stats}')
        self.device_info_list.append(f'CPU上下文切换/中断/软中断/系统调用次数: {cpu_stats}')

        cpu_times = psutil.cpu_times()
        print(f'CPU用户/系统/空闲/中断时间: {cpu_times}')
        self.device_info_list.append(f'CPU用户/系统/空闲/中断时间: {cpu_times}')

        cpu_times_percent = psutil.cpu_times_percent()
        print(f'CPU用户/系统/空闲/中断比例: {cpu_times_percent}')
        self.device_info_list.append(f'CPU用户/系统/空闲/中断比例: {cpu_times_percent}')

        # interval：表示每隔0.5s刷新一次
        # percpu：表示查看所有的cpu使用率
        cpu_percent = psutil.cpu_percent(interval=0.5, percpu=True)
        print(f'CPU使用率: {cpu_percent}')
        self.device_info_list.append(f'CPU使用率: {cpu_percent}')
        self.device_info_list.append("---------------------------------------------------------------------------------")

    def getMeminfo(self):
        virtual_memory = psutil.virtual_memory()
        print(f'内存信息: {virtual_memory}')
        self.device_info_list.append(f'内存信息: {virtual_memory}')
        swap_memory = psutil.swap_memory()
        print(f'内存交换信息: {swap_memory}')
        self.device_info_list.append(f'内存交换信息: {swap_memory}')
        self.device_info_list.append("---------------------------------------------------------------------------------")

    def getDiskinfo(self):
        disk_partitions = psutil.disk_partitions()
        print(f'磁盘分区/磁盘使用率/磁盘IO信息: {disk_partitions}')
        self.device_info_list.append(f'磁盘分区/磁盘使用率/磁盘IO信息: {disk_partitions}')
        disk_usage = psutil.disk_usage("C:\\")
        print(f'查看C磁盘使用信息: {disk_usage}')
        self.device_info_list.append(f'查看C磁盘使用信息: {disk_usage}')
        """
        read_count: 读次数
        write_count: 写次数
        read_bytes: 读的字节数
        write_bytes: 写的字节数
        read_time: 读时间
        write_time: 写时间 
        """
        disk_io_counters = psutil.disk_io_counters()
        print(f'磁盘IO统计信息: {disk_io_counters}')
        self.device_info_list.append(f'磁盘IO统计信息: {disk_io_counters}')

    def write_deviceinfo_to_file(self):
        file_utils.save_str_list_to_file(self.path_name, self.device_info_list, "a+")

if __name__ == "__main__":
    device_manager = DeviceManager('temp/device.txt')
    device_manager.getCpuinfo()
    device_manager.getMeminfo()
    device_manager.getDiskinfo()
    device_manager.write_deviceinfo_to_file()