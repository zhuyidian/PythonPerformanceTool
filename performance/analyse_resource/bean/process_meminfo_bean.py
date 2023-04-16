import time

class ProcessMeminfoBean:
    def __init__(self,name):
        self.pid_set = set()
        self.name = name
        self.time_list = []
        self.mem_list = []
        self.front_back_list = []

    def add_meminfo(self,pid,meminfo,time,front_or_back):
        self.mem_list.append(meminfo)
        # now = time.strftime("%H:%M:%S", time.localtime())
        self.time_list.append(time)
        self.pid_set.add(pid)
        self.front_back_list.append(front_or_back)