import time

class ProcessCpuinfoBean:
    def __init__(self,name):
        self.pid_set = set()
        self.name = name
        self.time_list = []
        self.cpu_list = []
        self.front_back_list = []

    def add_cpuinfo(self,pid,cpuinfo,time,front_or_back):
        self.cpu_list.append(cpuinfo)
        # now = time.strftime("%H:%M:%S", time.localtime())
        self.time_list.append(time)
        self.pid_set.add(pid)
        self.front_back_list.append(front_or_back)