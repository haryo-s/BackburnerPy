import ipaddress
from dataclasses import dataclass

@dataclass
class NetworkStatus:
    dropped_packets: int
    bad_packets: int
    tcp_requests: int
    udp_requests: int
    _boot_time: str

    # def get_total_memory(self):
    #     return self.total_memory
    
    # def get_total_memory_f(self):
    #     return self.get_total_memory_f

    # def get_num_cpus(self):
    #     return self.num_cpus

    #add parser for 2019/12/18-20:27:58:0597-03
    def get_boot_time(self):
        return None
        # try:
        #     return ipaddress.ip_address(_ip_address)
        # except:
        #     print('IP Address is invalid')

