import time

from analyse_resource.bean.process_cpuinfo_bean import ProcessCpuinfoBean
from analyse_resource.bean.process_meminfo_bean import ProcessMeminfoBean
from analyse_resource.bean.system_meminfo_bean import SystemMeminfoBean
from analyse_resource.excel.analyse_resource_excel import AnalyseResourceExcel
from analyse_resource.excel.analyse_resource_excel_data import AnalyseResourceExcelData
from analyse_resource.image.analyse_resource_image import AnalyseResourceImage
from analyse_resource.process_manager import ProcessManager
from utils import resource_utils, file_utils
from utils.analyse_data_utils import analyse_min_max_average
from utils.resource_utils import get_current_package_for_adb


class MeminfoManager:
    def __init__(self):
        self.collection_time_list = []
        self.system_meminfo_list = []
        self.process_meminfo_list = []
        self.analyse_resource_excel_data_list = []

    def add_system_meminfo_bean(self, systemmeminfobean):
        self.system_meminfo_list.append(systemmeminfobean)

    def add_process_meminfo_bean(self,pid,name,meminfo,time,front_back):
        find_flag = False
        bean:ProcessMeminfoBean= None

        for nn in self.process_meminfo_list:
            # print(f'add meminfo: name={name}, list name={nn.name}')
            if name == nn.name:
                find_flag = True
                bean = nn
                break
        if find_flag==True:   # add mem info
            bean.add_meminfo(pid,meminfo,time,front_back)
        else:
            new_bean = ProcessMeminfoBean(name)
            new_bean.add_meminfo(pid,meminfo,time,front_back)
            self.process_meminfo_list.append(new_bean)

    def analyse_meminfo_once(self,data_list,now,front_pid):
        for line_ in data_list:
            if type(line_) is str:
                line = line_.replace('\n', '').replace('\r', '')
            else:
                line = line_.decode().replace('\n', '').replace('\r', '')

            if "Total PSS by OOM adjustment" in line:
                break
            if 'pid' in line and 'kB' in line: # 进程
                # for name in process_list:
                # if name.name in line:
                mem_v = line.strip().split(':',1)[0].replace('kB', '').replace(',', '').strip()
                process_name = line.split(':',1)[1].split('(')[0].strip()
                pid = line.split('(pid')[1].split(')')[0].strip()
                process_pid = "".join(filter(str.isdigit, pid))
                # print(f'get meminfo: process_pid={process_pid},process_name={process_name},mem_v={mem_v}')
                if mem_v.isdigit() and process_pid.isdigit():
                    mem_v = round(float(mem_v) / 1024, 2)
                    front_back = 'b'
                    if process_pid==front_pid:
                        front_back = 'f'
                    self.add_process_meminfo_bean(process_pid, process_name, mem_v, now,front_back)
                else:
                    print(f'get meminfo: process parse error!!!!!!!!!!!!!!!!!!line={line}')
            elif 'pid' in line and 'K' in line:  # 进程
                mem_v = line.strip().split(':', 1)[0].replace('K', '').replace(',', '').strip()
                process_name = line.split(':', 1)[1].split('(')[0].strip()
                pid = line.split('(pid')[1].split(')')[0].strip()
                process_pid = "".join(filter(str.isdigit, pid))
                # print(f'get meminfo: process_pid={process_pid},process_name={process_name},mem_v={mem_v}')
                if mem_v.isdigit() and process_pid.isdigit():
                    mem_v = round(float(mem_v) / 1024, 2)
                    front_back = 'b'
                    if process_pid == front_pid:
                        front_back = 'f'
                    self.add_process_meminfo_bean(process_pid, process_name, mem_v, now,front_back)
                else:
                    print(f'get meminfo: process parse error!!!!!!!!!!!!!!!!!!line={line}')

        total_ram, free_ram, used_ram, lost_ram, free, used_pss, kernel,buffers, shmem, slab, total_swap, used_swap \
            = 0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00
        data_list.reverse()
        for line_ in data_list:
            if type(line_) is str:
                line = line_.replace('\n', '').replace('\r', '')
            else:
                line = line_.decode().replace('\n', '').replace('\r', '')

            if "Total PSS by category" in line:
                break
            if 'Total RAM' in line: # Total RAM
                # print(f'line={line}')
                ram = ''
                if 'K' in line:
                    ram = line.strip().split(':', 1)[1].split('K',1)[0].replace(',', '').strip()
                elif 'kB' in line:
                    ram = line.strip().split(':', 1)[1].split('kB', 1)[0].replace(',', '').strip()
                if ram.isdigit():
                    total_ram = round(float(ram) / 1024, 2)
                    # print(f'get meminfo: ram={ram}, total_ram={total_ram}')
                else:
                    print(f'get meminfo: total ram parse error!!!!!!!!!!!!!!!!!!line={line}')
            elif 'Free RAM' in line: # Free RAM
                # print(f'line={line}')
                ram = ''
                # free ram
                if 'K' in line:
                    ram = line.strip().split(':', 1)[1].split('K',1)[0].replace(',', '').strip()
                elif 'kB' in line:
                    ram = line.strip().split(':', 1)[1].split('kB', 1)[0].replace(',', '').strip()
                if ram.isdigit():
                    free_ram = round(float(ram) / 1024, 2)
                    # print(f'get meminfo: ram={ram}, free_ram={free_ram}')
                else:
                    print(f'get meminfo: free ram parse error!!!!!!!!!!!!!!!!!!line={line}')
                # free
                ram = ''
                if 'K' in line:
                    ram = line.strip().split(':', 1)[1].rsplit('free',1)[0].rsplit('+',1)[1]\
                        .replace(',', '').replace('K', '').strip()
                elif 'kB' in line:
                    ram = line.strip().split(':', 1)[1].rsplit('free',1)[0].rsplit('+',1)[1]\
                        .replace(',', '').replace('kB', '').strip()
                if ram.isdigit():
                    free = round(float(ram) / 1024, 2)
                    # print(f'get meminfo: ram={ram}, free={free}')
                else:
                    print(f'get meminfo: free parse error!!!!!!!!!!!!!!!!!!line={line}')
            elif 'Used RAM' in line: # Used RAM
                # print(f'line={line}')
                ram = ''
                # used ram
                if 'K' in line:
                    ram = line.strip().split(':', 1)[1].split('K', 1)[0].replace(',', '').strip()
                elif 'kB' in line:
                    ram = line.strip().split(':', 1)[1].split('kB', 1)[0].replace(',', '').strip()
                if ram.isdigit():
                    used_ram = round(float(ram) / 1024, 2)
                    # print(f'get meminfo: ram={ram}, used_ram={used_ram}')
                else:
                    print(f'get meminfo: used ram parse error!!!!!!!!!!!!!!!!!!line={line}')
                # used pss
                ram = ''
                if 'K' in line:
                    ram = line.strip().split(':', 1)[1].rsplit('used pss', 1)[0].rsplit('(', 1)[1] \
                        .replace(',', '').replace('K', '').strip()
                elif 'kB' in line:
                    ram = line.strip().split(':', 1)[1].rsplit('used pss', 1)[0].rsplit('(', 1)[1] \
                        .replace(',', '').replace('kB', '').strip()
                if ram.isdigit():
                    used_pss = round(float(ram) / 1024, 2)
                    # print(f'get meminfo: ram={ram}, used_pss={used_pss}')
                else:
                    print(f'get meminfo: used pss parse error!!!!!!!!!!!!!!!!!!line={line}')
                # kernel
                ram = ''
                if 'K' in line and 'kernel' in line:
                    ram = line.strip().split(':', 1)[1].rsplit('kernel', 1)[0].rsplit('+', 1)[1] \
                        .replace(',', '').replace('K', '').strip()
                    if ram.isdigit():
                        kernel = round(float(ram) / 1024, 2)
                        # print(f'get meminfo: ram={ram}, kernel={kernel}')
                    else:
                        print(f'get meminfo: kernel parse error!!!!!!!!!!!!!!!!!!line={line}')
                # buffers
                ram = ''
                if 'kB' in line and 'buffers' in line:
                    ram = line.strip().split(':', 1)[1].rsplit('buffers', 1)[0].rsplit('+', 1)[1] \
                        .replace(',', '').replace('kB', '').strip()
                    if ram.isdigit():
                        buffers = round(float(ram) / 1024, 2)
                        # print(f'get meminfo: ram={ram}, buffers={buffers}')
                    else:
                        print(f'get meminfo: buffers parse error!!!!!!!!!!!!!!!!!!line={line}')
                # shmem
                ram = ''
                if 'kB' in line and 'shmem' in line:
                    ram = line.strip().split(':', 1)[1].rsplit('shmem', 1)[0].rsplit('+', 1)[1] \
                        .replace(',', '').replace('kB', '').strip()
                    if ram.isdigit():
                        shmem = round(float(ram) / 1024, 2)
                        # print(f'get meminfo: ram={ram}, shmem={shmem}')
                    else:
                        print(f'get meminfo: shmem parse error!!!!!!!!!!!!!!!!!!line={line}')
                # slab
                ram = ''
                if 'kB' in line and 'slab' in line:
                    ram = line.strip().split(':', 1)[1].rsplit('slab', 1)[0].rsplit('+', 1)[1] \
                        .replace(',', '').replace('kB', '').strip()
                    if ram.isdigit():
                        slab = round(float(ram) / 1024, 2)
                        # print(f'get meminfo: ram={ram}, slab={slab}')
                    else:
                        print(f'get meminfo: slab parse error!!!!!!!!!!!!!!!!!!line={line}')
            elif 'Lost RAM' in line: # Lost RAM
                # print(f'line={line}')
                ram = ''
                if 'K' in line:
                    ram = line.strip().split(':', 1)[1].split('K', 1)[0].replace(',', '').strip()
                elif 'kB' in line:
                    ram = line.strip().split(':', 1)[1].split('kB', 1)[0].replace(',', '').strip()
                if ram.isdigit():
                    lost_ram = round(float(ram) / 1024, 2)
                    # print(f'get meminfo: ram={ram}, lost_ram={lost_ram}')
                else:
                    print(f'get meminfo: lost ram parse error!!!!!!!!!!!!!!!!!!line={line}')
            elif 'ZRAM' in line and 'total swap' in line: # ZRAM
                # print(f'line={line}')
                ram = ''
                # total_swap
                if 'K' in line:
                    ram = line.strip().split(':', 1)[1].rsplit('total swap', 1)[0].rsplit('(', 1)[1] \
                        .replace(',', '').replace('K', '').strip()
                elif 'kB' in line:
                    ram = line.strip().split(':', 1)[1].rsplit('total swap', 1)[0].rsplit('(', 1)[1] \
                        .replace(',', '').replace('kB', '').strip()
                if ram.isdigit():
                    total_swap = round(float(ram) / 1024, 2)
                    # print(f'get meminfo: ram={ram}, total_swap={total_swap}')
                else:
                    print(f'get meminfo: total swap parse error!!!!!!!!!!!!!!!!!!line={line}')
                # used swap
                ram = ''
                if 'K' in line:
                    ram_list = line.strip().split(':', 1)[1].rsplit('in swap', 1)[0].split()
                    # print(f'get meminfo: ram_list={ram_list}')
                    ram_list.reverse()
                    for rr in ram_list:
                        if ('K' in rr) or (rr.isdigit()):
                            ram = rr.replace(',', '').replace('K', '').strip()
                            break
                elif 'kB' in line:
                    ram_list = line.strip().split(':', 1)[1].rsplit('in swap', 1)[0].split('used', 1)[1].split()
                    # print(f'get meminfo: ram_list={ram_list}')
                    ram_list.reverse()
                    for rr in ram_list:
                        if ('kB' in rr) or (rr.isdigit()):
                            ram1 = rr.replace(',', '').replace('kB', '').strip()
                            if ram1.isdigit():
                                ram = ram1
                                break
                if ram.isdigit():
                    used_swap = round(float(ram) / 1024, 2)
                    # print(f'get meminfo: ram={ram}, used_swap={used_swap}')
                else:
                    print(f'get meminfo: used swap parse error!!!!!!!!!!!!!!!!!!line={line}')
        # print(f'get meminfo: parse OK total_ram={total_ram},free_ram={free_ram},used_ram={used_ram},lost_ram={lost_ram},free={free},'
        #       f'used_pss={used_pss},kernel={kernel},buffers={buffers},shmem={shmem},slab={slab},total_swap={total_swap},used_swap={used_swap}')
        self.add_system_meminfo_bean(SystemMeminfoBean(total_ram, free_ram, used_ram, lost_ram, free, used_pss, kernel,
                                                       buffers,shmem,slab,total_swap,used_swap))

    def get_meminfo_once(self, path_name=''):
        now = time.strftime("%H:%M:%S", time.localtime())
        self.collection_time_list.append(now)
        top_adb = resource_utils.get_meminfo_for_adb().stdout.readlines()
        if len(path_name)!=0:
            file_utils.save_list_to_file(path_name,top_adb,"a+")
        # 判断前后台
        front_pid, front_package_name = get_current_package_for_adb()
        print(f"当前运行的进程为: {front_pid}, {front_package_name}")
        self.analyse_meminfo_once(top_adb,now,front_pid)

    def get_meminfo_once_test(self, file_name):
        now = time.strftime("%H:%M:%S", time.localtime())
        self.collection_time_list.append(now)
        f = open(file_name, encoding="utf-8", mode="r")
        # f = open(r'ip.txt', 'r')
        file_list = list(f)
        self.analyse_meminfo_once(file_list, now,'')
        f.close()

    def write_to_excel(self, excel_path_name, txt_path_name, analyse_resource_image: AnalyseResourceImage):
        # print(f'write to excel: excel_path_name={excel_path_name},txt_path_name={txt_path_name}')
        file = open(txt_path_name, "a+")

        total_ram_highs, free_ram_highs, used_ram_highs, lost_ram_highs, free_highs, used_pss_highs, kernel_highs, buffers_highs, \
            shmem_highs, slab_highs, total_swap_highs, used_swap_highs = [], [], [], [], [], [], [], [], [], [], [], []
        for bean in self.system_meminfo_list:
            total_ram_highs.append(bean.total_ram)
            free_ram_highs.append(bean.free_ram)
            used_ram_highs.append(bean.used_ram)
            lost_ram_highs.append(bean.lost_ram)
            free_highs.append(bean.free)
            used_pss_highs.append(bean.used_pss)
            kernel_highs.append(bean.kernel)
            buffers_highs.append(bean.buffers)
            shmem_highs.append(bean.shmem)
            slab_highs.append(bean.slab)
            total_swap_highs.append(bean.total_swap)
            used_swap_highs.append(bean.used_swap)
        min, max, average = analyse_min_max_average(list(map(float, total_ram_highs)))
        self.analyse_resource_excel_data_list.append(AnalyseResourceExcelData('',"total_ram", min, max, average))
        # 写文件
        total_ram_highs_str = ['{:.2f}'.format(x) for x in total_ram_highs]
        file.write('total_ram(MB): ' + (','.join(total_ram_highs_str)) + '\n')
        file.write('total_ram(MB): ' + f'min({min}) ' + f'max({max}) ' + f'average({average})' + '\n')
        # 生成image
        analyse_resource_image.do_meminfo_image('total_ram.jpg', 'total_ram', self.collection_time_list, list(map(float, total_ram_highs)), min,
                                        max, average)

        min, max, average = analyse_min_max_average(list(map(float, free_ram_highs)))
        self.analyse_resource_excel_data_list.append(AnalyseResourceExcelData('',"free_ram", min, max, average))
        # 写文件
        free_ram_highs_str = ['{:.2f}'.format(x) for x in free_ram_highs]
        file.write('free_ram(MB): ' + (','.join(free_ram_highs_str)) + '\n')
        file.write('free_ram(MB): ' + f'min({min}) ' + f'max({max}) ' + f'average({average})' + '\n')
        # 生成image
        analyse_resource_image.do_meminfo_image('free_ram.jpg', 'free_ram', self.collection_time_list,
                                                list(map(float, free_ram_highs)), min,
                                                max, average)

        min, max, average = analyse_min_max_average(list(map(float, used_ram_highs)))
        self.analyse_resource_excel_data_list.append(AnalyseResourceExcelData('',"used_ram", min, max, average))
        # 写文件
        used_ram_highs_str = ['{:.2f}'.format(x) for x in used_ram_highs]
        file.write('used_ram(MB): ' + (','.join(used_ram_highs_str)) + '\n')
        file.write('used_ram(MB): ' + f'min({min}) ' + f'max({max}) ' + f'average({average})' + '\n')
        # 生成image
        analyse_resource_image.do_meminfo_image('used_ram.jpg', 'used_ram', self.collection_time_list,
                                                list(map(float, used_ram_highs)), min,
                                                max, average)

        min, max, average = analyse_min_max_average(list(map(float, lost_ram_highs)))
        self.analyse_resource_excel_data_list.append(AnalyseResourceExcelData('',"lost_ram", min, max, average))
        # 写文件
        lost_ram_highs_str = ['{:.2f}'.format(x) for x in lost_ram_highs]
        file.write('lost_ram(MB): ' + (','.join(lost_ram_highs_str)) + '\n')
        file.write('lost_ram(MB): ' + f'min({min}) ' + f'max({max}) ' + f'average({average})' + '\n')
        # 生成image
        analyse_resource_image.do_meminfo_image('lost_ram.jpg', 'lost_ram', self.collection_time_list,
                                                list(map(float, lost_ram_highs)), min,
                                                max, average)

        min, max, average = analyse_min_max_average(list(map(float, free_highs)))
        self.analyse_resource_excel_data_list.append(AnalyseResourceExcelData('',"free", min, max, average))
        # 写文件
        free_highs_str = ['{:.2f}'.format(x) for x in free_highs]
        file.write('free(MB): ' + (','.join(free_highs_str)) + '\n')
        file.write('free(MB): ' + f'min({min}) ' + f'max({max}) ' + f'average({average})' + '\n')
        # 生成image
        analyse_resource_image.do_meminfo_image('free.jpg', 'free', self.collection_time_list,
                                                list(map(float, free_highs)), min,
                                                max, average)

        min, max, average = analyse_min_max_average(list(map(float, used_pss_highs)))
        self.analyse_resource_excel_data_list.append(AnalyseResourceExcelData('',"used_pss", min, max, average))
        # 写文件
        used_pss_highs_str = ['{:.2f}'.format(x) for x in used_pss_highs]
        file.write('used_pss(MB): ' + (','.join(used_pss_highs_str)) + '\n')
        file.write('used_pss(MB): ' + f'min({min}) ' + f'max({max}) ' + f'average({average})' + '\n')
        # 生成image
        analyse_resource_image.do_meminfo_image('used_pss.jpg', 'used_pss', self.collection_time_list,
                                                list(map(float, used_pss_highs)), min,
                                                max, average)

        min, max, average = analyse_min_max_average(list(map(float, kernel_highs)))
        self.analyse_resource_excel_data_list.append(AnalyseResourceExcelData('',"kernel", min, max, average))
        # 写文件
        kernel_highs_str = ['{:.2f}'.format(x) for x in kernel_highs]
        file.write('kernel(MB): ' + (','.join(kernel_highs_str)) + '\n')
        file.write('kernel(MB): ' + f'min({min}) ' + f'max({max}) ' + f'average({average})' + '\n')
        # 生成image
        analyse_resource_image.do_meminfo_image('kernel.jpg', 'kernel', self.collection_time_list,
                                                list(map(float, kernel_highs)), min,
                                                max, average)

        min, max, average = analyse_min_max_average(list(map(float, buffers_highs)))
        self.analyse_resource_excel_data_list.append(AnalyseResourceExcelData('',"buffers", min, max, average))
        # 写文件
        buffers_highs_str = ['{:.2f}'.format(x) for x in buffers_highs]
        file.write('buffers(MB): ' + (','.join(buffers_highs_str)) + '\n')
        file.write('buffers(MB): ' + f'min({min}) ' + f'max({max}) ' + f'average({average})' + '\n')
        # 生成image
        analyse_resource_image.do_meminfo_image('buffers.jpg', 'buffers', self.collection_time_list,
                                                list(map(float, buffers_highs)), min,
                                                max, average)

        min, max, average = analyse_min_max_average(list(map(float, shmem_highs)))
        self.analyse_resource_excel_data_list.append(AnalyseResourceExcelData('',"shmem", min, max, average))
        # 写文件
        shmem_highs_str = ['{:.2f}'.format(x) for x in shmem_highs]
        file.write('shmem(MB): ' + (','.join(shmem_highs_str)) + '\n')
        file.write('shmem(MB): ' + f'min({min}) ' + f'max({max}) ' + f'average({average})' + '\n')
        # 生成image
        analyse_resource_image.do_meminfo_image('shmem.jpg', 'shmem', self.collection_time_list,
                                                list(map(float, shmem_highs)), min,
                                                max, average)

        min, max, average = analyse_min_max_average(list(map(float, slab_highs)))
        self.analyse_resource_excel_data_list.append(AnalyseResourceExcelData('',"slab", min, max, average))
        # 写文件
        slab_highs_str = ['{:.2f}'.format(x) for x in slab_highs]
        file.write('slab(MB): ' + (','.join(slab_highs_str)) + '\n')
        file.write('slab(MB): ' + f'min({min}) ' + f'max({max}) ' + f'average({average})' + '\n')
        # 生成image
        analyse_resource_image.do_meminfo_image('slab.jpg', 'slab', self.collection_time_list,
                                                list(map(float, slab_highs)), min,
                                                max, average)

        min, max, average = analyse_min_max_average(list(map(float, total_swap_highs)))
        self.analyse_resource_excel_data_list.append(AnalyseResourceExcelData('',"total_swap", min, max, average))
        # 写文件
        total_swap_highs_str = ['{:.2f}'.format(x) for x in total_swap_highs]
        file.write('total_swap(MB): ' + (','.join(total_swap_highs_str)) + '\n')
        file.write('total_swap(MB): ' + f'min({min}) ' + f'max({max}) ' + f'average({average})' + '\n')
        # 生成image
        analyse_resource_image.do_meminfo_image('total_swap.jpg', 'total_swap', self.collection_time_list,
                                                list(map(float, total_swap_highs)), min,
                                                max, average)

        min, max, average = analyse_min_max_average(list(map(float, used_swap_highs)))
        self.analyse_resource_excel_data_list.append(AnalyseResourceExcelData('',"used_swap", min, max, average))
        # 写文件
        used_swap_highs_str = ['{:.2f}'.format(x) for x in used_swap_highs]
        file.write('used_swap(MB): ' + (','.join(used_swap_highs_str)) + '\n')
        file.write('used_swap(MB): ' + f'min({min}) ' + f'max({max}) ' + f'average({average})' + '\n')
        # 生成image
        analyse_resource_image.do_meminfo_image('used_swap.jpg', 'used_swap', self.collection_time_list,
                                                list(map(float, used_swap_highs)), min,
                                                max, average)

        for bean in self.process_meminfo_list:
            process_highs = []
            process_name = bean.name
            for mem in bean.mem_list:
                process_highs.append(mem)
            min, max, average = analyse_min_max_average(list(map(float, process_highs)))
            self.analyse_resource_excel_data_list.append(AnalyseResourceExcelData(' '.join(bean.pid_set),process_name, min, max, average))
            # 写文件
            process_highs_str = ['{:.2f}'.format(x) for x in process_highs]
            file.write(f'{bean.pid_set} ' + f'{process_name}(MB): ' + (','.join(process_highs_str)) + '\n')
            file.write(f'{bean.pid_set} ' + f'{process_name}(MB): ' + f'min({min}) ' + f'max({max}) ' + f'average({average})' + '\n')
            # 生成image
            x_list = []
            for i in range(len(bean.time_list)):
                value = bean.front_back_list[i] + ' ' + bean.time_list[i]
                x_list.append(value)
            analyse_resource_image.do_meminfo_image(f'{process_name}.jpg', process_name, x_list, list(map(float, process_highs)),min,max,average)

        file.close()
        analyse_resource_excel = AnalyseResourceExcel(excel_path_name,'mem')
        # write first row
        head_data_list = ['name','mem_min(MB)','mem_max(MB)','mem_average(MB)']
        analyse_resource_excel.write_first_row_data(head_data_list)
        # write rows
        analyse_resource_excel.write_rows_data(self.analyse_resource_excel_data_list)

if __name__ == "__main__":
    meminfo_manager = MeminfoManager()
    for i in range(1):
        meminfo_manager.get_meminfo_once()   # 连接adb方式测试
        # meminfo_manager.get_meminfo_once_test('sample/dumpsys_meminfo_2') # 使用文件方式测试

    for bean in meminfo_manager.system_meminfo_list:
        print(
            f'system meminfo list: total_ram={bean.total_ram}, free_ram={bean.free_ram}, used_ram={bean.used_ram}, lost_ram={bean.lost_ram},'
            f'free={bean.free},used_pss={bean.used_pss},kernel={bean.kernel},buffers={bean.buffers},shmem={bean.shmem},'
            f',slab={bean.slab},total_swap={bean.total_swap},used_swap={bean.used_swap}')
    for bean in meminfo_manager.process_meminfo_list:
        print(f'process meminfo list: pid={bean.pid_set}, name={bean.name}, mem_list={bean.mem_list}')