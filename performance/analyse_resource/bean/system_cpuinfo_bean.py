
class SystemCpuinfoBean:
    def __init__(self,usr,sys,nic,idle,io,irq,sirq):
        self.usr = usr
        self.sys = sys
        self.nic = nic
        self.idle = idle
        self.io = io
        self.irq = irq
        self.sirq = sirq