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

from utils.resource_utils import get_current_package_for_adb


class CpuinfoManager:
    def __init__(self):
        self.collection_time_list = []
        self.system_cpuinfo_list = []
        self.process_cpuinfo_list = []
        self.analyse_resource_excel_data_list = []

    def add_system_cpuinfo_bean(self, systemcpuinfobean):
        self.system_cpuinfo_list.append(systemcpuinfobean)

    def add_process_cpuinfo_bean(self,pid,name,cpuinfo,time,front_back):
        find_flag = False
        bean:ProcessCpuinfoBean= None
        for nn in self.process_cpuinfo_list:
            if name in nn.name:
                find_flag = True
                bean = nn
                break
        if find_flag==True:   # add cpu info
            bean.add_cpuinfo(pid,cpuinfo,time,front_back)
        else:
            new_bean = ProcessCpuinfoBean(name)
            new_bean.add_cpuinfo(pid,cpuinfo,time,front_back)
            self.process_cpuinfo_list.append(new_bean)

    def analyse_cpuinfo_once(self,data_list,now,front_pid):
        for line_ in data_list:
            # print(f'analyse cpuinfo: line_ type={type(line_)}')
            if type(line_) is str:
                line = line_.replace('\n', '').replace('\r', '')
            else:
                # print(f'analyse cpuinfo: line_ type={type(line_)},222222222222222')
                line = line_.decode().replace('\n','').replace('\r', '')
            # print(f'analyse cpuinfo: line:={line}')
            # print(f'analyse cpuinfo: line_list={line.split()}')
            if 'Using fallback' in line:  # 首行
                pass
            elif 'used' in line and 'free' in line: # 第二行
                pass
            elif 'CPU' in line and 'idle' in line:  # 系统CPU
                usr_cpu = resource_utils.extract_system_cpuinfo(line, 'usr')
                sys_cpu = resource_utils.extract_system_cpuinfo(line, 'sys')
                nic_cpu = resource_utils.extract_system_cpuinfo(line, 'nic')
                idle_cpu = resource_utils.extract_system_cpuinfo(line, 'idle')
                io_cpu = resource_utils.extract_system_cpuinfo(line, 'io')
                irq_cpu = resource_utils.extract_system_cpuinfo(line, 'irq')
                sirq_cpu = resource_utils.extract_system_cpuinfo(line, 'sirq')
                # print(f'analyse cpuinfo: usr_cpu={usr_cpu},sys_cpu={sys_cpu},nic_cpu={nic_cpu},idle_cpu={idle_cpu},'
                #       f'io_cpu={io_cpu},irq_cpu={irq_cpu},sirq_cpu={sirq_cpu},')
                self.add_system_cpuinfo_bean(SystemCpuinfoBean(usr_cpu,sys_cpu,nic_cpu,idle_cpu,io_cpu,irq_cpu,sirq_cpu))
            elif 'Load average' in line: # 第四行
                pass
            elif 'PID' in line and 'USER' in line:
                pass
            else: # 进程
                # 规则1：根据进程名截取，进程名前面就是cpu。缺点：进程名不能完全匹配
                # line_list = line.split()
                # find_flag = False
                # print(f'top process line={line_list}')
                # for name in process_list:
                #     if name.name in line:
                #         process_pid = line_list[0]
                #         procass_cpu = resource_utils.extract_system_cpuinfo(line, name.name)
                #         # print(f'find process: process={name.name}, procass_cpu={procass_cpu}')
                #         self.add_process_cpuinfo_bean(process_pid, name.name, procass_cpu,now)
                #         find_flag = True
                #         break
                # if find_flag==False:
                #     print(f'not find process: !!!!!!!!!line={line}')
                # 规则2：根据最后一个浮点数，是否再根据连续3个数字进行判断?放在后面有问题再兼容
                if '%' in line:
                    line_list = line.split()
                    # print(f'analyse cpuinfo: process line={line}')
                    # print(f'analyse cpuinfo: process line_list={line_list}')
                    process_pid = line_list[0]
                    line_list.reverse()
                    process_name = ''
                    process_cpu = ''
                    find_cpu = False
                    for i in range(len(line_list)):
                        if '%' in line_list[i]:
                            cpu1 = line_list[i].strip('%').strip()
                            if analyse_str_is_float_or_int(cpu1):
                                process_cpu = cpu1
                                find_cpu = True
                                break
                        process_name += line_list[i]
                    if find_cpu == True:
                        # print(f'analyse cpuinfo:  process_pid={process_pid},process_name={process_name},process_cpu={process_cpu}')
                        front_back = 'b'
                        if process_pid == front_pid:
                            front_back = 'f'
                        self.add_process_cpuinfo_bean(process_pid, process_name, process_cpu, now,front_back)
                    else:
                        print(f'analyse cpuinfo:  cpu parse error!!!!!!!!!line={line}')
                else:
                    line_list = line.split()
                    # print(f'analyse cpuinfo: process line={line}')
                    # print(f'analyse cpuinfo: process line_list={line_list}')
                    process_pid = line_list[0]
                    line_list.reverse()
                    process_name = ''
                    process_cpu = ''
                    find_cpu = False
                    for i in range(len(line_list)):
                        if analyse_str_is_float(line_list[i]):
                            process_cpu = line_list[i]
                            find_cpu = True
                            break
                        process_name += line_list[i]
                    if find_cpu==True:
                        # print(f'analyse cpuinfo:  process_pid={process_pid},process_name={process_name},process_cpu={process_cpu}')
                        front_back = 'b'
                        if process_pid == front_pid:
                            front_back = 'f'
                        self.add_process_cpuinfo_bean(process_pid, process_name, process_cpu, now,front_back)
                    else:
                        print(f'analyse cpuinfo:  cpu parse error!!!!!!!!!line={line}')

    def get_cpuinfo_once(self,path_name=''):
        now = time.strftime("%H:%M:%S", time.localtime())
        self.collection_time_list.append(now)
        top_adb = resource_utils.get_cpuinfo_for_adb().stdout.readlines()
        if len(path_name)!=0:
            file_utils.save_list_to_file(path_name,top_adb,"a+")
        # 判断前后台
        front_pid, front_package_name = get_current_package_for_adb()
        print(f"当前运行的进程为: {front_pid}, {front_package_name}")
        self.analyse_cpuinfo_once(top_adb,now,front_pid)

    def get_cpuinfo_once_test(self,file_name):
        now = time.strftime("%H:%M:%S", time.localtime())
        self.collection_time_list.append(now)
        f = open(file_name, encoding="utf-8", mode="r")
        # f = open(r'ip.txt', 'r')
        file_list = list(f)
        self.analyse_cpuinfo_once(file_list,now)
        f.close()

    def write_to_excel(self,excel_path_name,txt_path_name,analyse_resource_image:AnalyseResourceImage,target_keywords,target_path,target_path_name):
        # print(f'write to excel: excel_path_name={excel_path_name},txt_path_name={txt_path_name}')
        file = open(txt_path_name, "a+")
        file_target = open(target_path_name, "a+")

        usr_highs,sys_highs,nic_highs,idle_highs,io_highs,irq_highs,sirq_highs = [],[],[],[],[],[],[]
        for bean in self.system_cpuinfo_list:
            usr_highs.append(bean.usr.strip('%'))
            sys_highs.append(bean.sys.strip('%'))
            nic_highs.append(bean.nic.strip('%'))
            idle_highs.append(bean.idle.strip('%'))
            io_highs.append(bean.io.strip('%'))
            irq_highs.append(bean.irq.strip('%'))
            sirq_highs.append(bean.sirq.strip('%'))

        min,max,average = analyse_min_max_average(list(map(float, usr_highs)))
        self.analyse_resource_excel_data_list.append(AnalyseResourceExcelData('',"usr",min,max,average))
        # 写文件
        file.write('usr: ' + (','.join(usr_highs)) + '\n')
        file.write('usr: ' + f'min({min}) ' + f'max({max}) ' + f'average({average})' + '\n')
        # 生成image
        analyse_resource_image.do_cpuinfo_image('usr.jpg','usr',self.collection_time_list,list(map(float, usr_highs)),min,max,average,target_keywords,target_path)

        min, max, average = analyse_min_max_average(list(map(float, sys_highs)))
        self.analyse_resource_excel_data_list.append(AnalyseResourceExcelData('',"sys", min, max, average))
        # 写文件
        file.write('sys: ' + (','.join(sys_highs)) + '\n')
        file.write('sys: ' + f'min({min}) ' + f'max({max}) ' + f'average({average})' + '\n')
        # 生成image
        analyse_resource_image.do_cpuinfo_image('sys.jpg', 'sys', self.collection_time_list, list(map(float, sys_highs)),min,max,average,target_keywords,target_path)

        min, max, average = analyse_min_max_average(list(map(float, nic_highs)))
        self.analyse_resource_excel_data_list.append(AnalyseResourceExcelData('',"nic", min, max, average))
        # 写文件
        file.write('nic: ' + (','.join(nic_highs)) + '\n')
        file.write('nic: ' + f'min({min}) ' + f'max({max}) ' + f'average({average})' + '\n')
        # 生成image
        analyse_resource_image.do_cpuinfo_image('nic.jpg', 'nic', self.collection_time_list, list(map(float, nic_highs)),min,max,average,target_keywords,target_path)

        min, max, average = analyse_min_max_average(list(map(float, idle_highs)))
        self.analyse_resource_excel_data_list.append(AnalyseResourceExcelData('',"idle", min, max, average))
        # 写文件
        file.write('idle: ' + (','.join(idle_highs)) + '\n')
        file.write('idle: ' + f'min({min}) ' + f'max({max}) ' + f'average({average})' + '\n')
        # 生成image
        analyse_resource_image.do_cpuinfo_image('idle.jpg', 'idle', self.collection_time_list, list(map(float, idle_highs)),min,max,average,target_keywords,target_path)

        min, max, average = analyse_min_max_average(list(map(float, io_highs)))
        self.analyse_resource_excel_data_list.append(AnalyseResourceExcelData('',"io", min, max, average))
        # 写文件
        file.write('io: ' + (','.join(io_highs)) + '\n')
        file.write('io: ' + f'min({min}) ' + f'max({max}) ' + f'average({average})' + '\n')
        # 生成image
        analyse_resource_image.do_cpuinfo_image('io.jpg', 'io', self.collection_time_list, list(map(float, io_highs)),min,max,average,target_keywords,target_path)

        min, max, average = analyse_min_max_average(list(map(float, irq_highs)))
        self.analyse_resource_excel_data_list.append(AnalyseResourceExcelData('',"irq", min, max, average))
        # 写文件
        file.write('irq: ' + (','.join(irq_highs)) + '\n')
        file.write('irq: ' + f'min({min}) ' + f'max({max}) ' + f'average({average})' + '\n')
        # 生成image
        analyse_resource_image.do_cpuinfo_image('irq.jpg', 'irq', self.collection_time_list, list(map(float, irq_highs)),min,max,average,target_keywords,target_path)

        min, max, average = analyse_min_max_average(list(map(float, sirq_highs)))
        self.analyse_resource_excel_data_list.append(AnalyseResourceExcelData('',"sirq", min, max, average))
        # 写文件
        file.write('sirq: ' + (','.join(sirq_highs)) + '\n')
        file.write('sirq: ' + f'min({min}) ' + f'max({max}) ' + f'average({average})' + '\n')
        # 生成image
        analyse_resource_image.do_cpuinfo_image('sirq.jpg', 'sirq', self.collection_time_list, list(map(float, sirq_highs)),min,max,average,target_keywords,target_path)

        for bean in self.process_cpuinfo_list:
            process_highs = []
            process_name = bean.name
            for cpu in bean.cpu_list:
                process_highs.append(cpu.strip('%'))
            # process_highs.append(bean.cpu_list)
            min, max, average = analyse_min_max_average(list(map(float, process_highs)))
            self.analyse_resource_excel_data_list.append(AnalyseResourceExcelData(' '.join(bean.pid_set),process_name, min, max, average))
            # 写文件
            file.write(f'{bean.pid_set} ' + f'{process_name}: ' + (','.join(process_highs)) + '\n')
            file.write(f'{bean.pid_set} ' + f'{process_name}: ' + f'min({min}) ' + f'max({max}) ' + f'average({average})' + '\n')
            #print(f'write_to_excel: process_name={process_name}, target_keywords={target_keywords}')
            if target_keywords in process_name:
                file_target.write(f'{bean.pid_set} ' + f'{process_name}: ' + (','.join(process_highs)) + '\n')
                file_target.write(
                    f'{bean.pid_set} ' + f'{process_name}: ' + f'min({min}) ' + f'max({max}) ' + f'average({average})' + '\n')
            # 生成image
            x_list = []
            for i in range(len(bean.time_list)):
                value = bean.front_back_list[i] + ' ' + bean.time_list[i]
                x_list.append(value)
            analyse_resource_image.do_cpuinfo_image(f'{process_name}.jpg', process_name, x_list, list(map(float, process_highs)),min,max,average,target_keywords,target_path)

        file.close()
        file_target.close()
        analyse_resource_excel = AnalyseResourceExcel(excel_path_name,'cpu')
        # write first row
        head_data_list = ['pid','name','cpu_min','cpu_max','cpu_average']
        analyse_resource_excel.write_first_row_data(head_data_list)
        # write rows
        analyse_resource_excel.write_rows_data(self.analyse_resource_excel_data_list)

if __name__ == "__main__":
    cpuinfo_manager = CpuinfoManager()
    for i in range(1):
        # cpuinfo_manager.get_cpuinfo_once()  # 连接adb方式测试
        cpuinfo_manager.get_cpuinfo_once_test('sample/top_2') # 使用文件方式测试

    for bean in cpuinfo_manager.system_cpuinfo_list:
        print(f'system cpuinfo list: usr={bean.usr}, sys={bean.sys}, nic={bean.nic}, idle={bean.idle},'
              f'io={bean.io},irq={bean.irq},sirq={bean.sirq}')
    for bean in cpuinfo_manager.process_cpuinfo_list:
        print(f'process cpuinfo list: pid={bean.pid_set}, name={bean.name}, cpu_list={bean.cpu_list}')