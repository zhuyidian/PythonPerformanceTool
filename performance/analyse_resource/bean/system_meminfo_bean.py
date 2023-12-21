
class SystemMeminfoBean:
    def __init__(self,total_ram,free_ram,used_ram,lost_ram,free,used_pss,kernel,buffers,shmem,slab,total_swap,used_swap):
        self.total_ram = total_ram
        self.free_ram = free_ram
        self.used_ram = used_ram
        self.lost_ram = lost_ram
        self.free = free
        self.used_pss = used_pss
        self.kernel = kernel
        self.buffers = buffers
        self.shmem = shmem
        self.slab = slab
        self.total_swap = total_swap
        self.used_swap = used_swap