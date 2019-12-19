from dataclasses import dataclass
import ipaddress

@dataclass
class NetworkStatus:
    dropped_packets: int
    bad_packets: int
    tcp_requests: int
    udp_requests: int
    _boot_time: str

    # TODO: add parser for 2019/12/18-20:27:58:0597-03
    def get_boot_time(self):
        return None
        # try:
        #     return ipaddress.ip_address(_ip_address)
        # except:
        #     print('IP Address is invalid')

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

@dataclass
class HardwareInfo:
    total_memory: int
    total_memory_f: float
    num_cpus: int
    platform: str
    workdisk_space: int
    mac: str

@dataclass
class BackburnerManagerInfo:
    version: int
    servers: int
    jobs: int
    system_info: SystemInfo
    network_status: NetworkStatus

@dataclass 
class Client:
    version: int
    udp_port: int
    controller: bool
    system_info: SystemInfo

@dataclass
class Plugin:
    version: int
    name: str
    description: str

@dataclass
class ServerSchedule:
    sunday: int
    monday: int
    tuesday: int
    wednesday: int
    thursday: int
    friday: int
    saturday: int

@dataclass
class ServerListItem:
    handle: str
    state: int
    name: str

@dataclass 
class Server:
    version: int
    name: str
    user_name: str
    total_task: int
    total_time: float
    perf_index: float
    _ip_address: str
    current_status: int
    hw_info: HardwareInfo
    network_status: NetworkStatus
    server_schedule: ServerSchedule
    att_priority: bool
    una_priority: bool
    current_job: int #TODO: Check this, it might also be a hex string
    current_task: int
    task_started: str
    plugins: list
