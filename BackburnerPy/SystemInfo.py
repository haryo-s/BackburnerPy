import ipaddress
from dataclasses import dataclass

@dataclass
class SystemInfo:
    total_memory: int
    total_memory_f: float
    num_cpus: int
    platform: str
    user: str
    computer_name: str
    mac: str
    workdisk_space: int
    _ip_address: str

    # def get_total_memory(self):
    #     return self.total_memory
    
    # def get_total_memory_f(self):
    #     return self.get_total_memory_f

    # def get_num_cpus(self):
    #     return self.num_cpus

            