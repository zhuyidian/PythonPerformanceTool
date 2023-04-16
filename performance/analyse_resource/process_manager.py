from analyse_resource.bean.process_bean import ProcessBean
from utils import resource_utils
from utils import file_utils

class ProcessManager:
    def __init__(self):
        self.process_list = []

    def get_process_all(self,path_name):
        process_adb = resource_utils.get_process_all_for_adb().stdout.readlines()
        file_utils.save_list_to_file(path_name,process_adb,"w")

        for line in process_adb[1:]:
            line = line.decode().replace('\n','').replace('\r', '')
            line_list = line.split()
            # print(f'get process line: {line}')
            # print(f'get process line_list: {line.split()}')
            self.add_process_bean(ProcessBean(line_list[1], line_list[8]))

    def add_process_bean(self,processbean):
        self.process_list.append(processbean)





if __name__ == "__main__":
    # 使用ps命令获取所有进程
    process_manager = ProcessManager()
    process_manager.get_process_all()
    for bean in process_manager.process_list:
        print(f'process list: pid={bean.pid}, name={bean.name}')