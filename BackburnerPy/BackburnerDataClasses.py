from dataclasses import dataclass
import ipaddress

@dataclass
class NetworkStatus:
    """Backburner Manager network status"""
    dropped_packets: int
    bad_packets: int
    tcp_requests: int
    udp_requests: int
    _boot_time: str

@dataclass
class SystemInfo:
    """Backburner Manager system information"""
    total_memory: int
    total_memory_f: float
    num_cpus: int
    platform: str
    user: str
    computer_name: str
    mac: str
    workdisk_space: int
    _ip_address: str

@dataclass
class HardwareInfo:
    """Backburner Manager hardware information"""
    total_memory: int
    total_memory_f: float
    num_cpus: int
    platform: str
    workdisk_space: int
    mac: str

@dataclass
class BackburnerManagerInfo:
    """Backburner Manager information"""
    version: int
    servers: int
    jobs: int
    system_info: SystemInfo
    network_status: NetworkStatus

@dataclass 
class Client:
    """Client information"""
    version: int
    udp_port: int
    controller: bool
    system_info: SystemInfo

@dataclass
class Plugin:
    """Plugin information"""
    version: int
    name: str
    description: str

@dataclass 
class JobListItem:
    """Job item in list"""
    handle: int
    state: int

@dataclass
class JobInfo:
    """Job information"""
    version: int
    job_handle: int
    name: str
    description: str
    job_priority: int
    user: str
    computer: str
    last_updated: str
    submitted: str
    started: str
    ended: str
    number_tasks: int
    tasks_completed: int
    encoding: str

@dataclass 
class JobFlags:
    """Job flags"""
    active: bool
    complete: bool
    nonconcurrent: bool
    nonstoppable: bool
    ignore_job_share: bool
    job_has_dependencies: bool
    zip_archive: bool
    leave_in_queue: bool
    archive_when_done: bool
    delete_when_done: bool
    override_blocking_tasks: bool
    enable_blocking_tasks: bool

@dataclass 
class JobPlugin:
    """Job plugin information"""
    plugin_name: str
    plugin_version: int

@dataclass
class JobAlerts:
    """Job alert settings"""
    enabled: bool
    failure: bool
    progress: bool
    completion: bool
    nth_task: int
    send_email: bool
    include_summary: bool
    email_from: str
    email_to: str
    email_server: str

@dataclass
class JobServerList:
    """Job server list settings"""
    all: bool

@dataclass
class JobServer:
    """Job server information"""
    handle: str
    active: bool
    task_time: float
    task_total: int
    context_switch: int
    rt_failed: bool

@dataclass 
class Job:
    """Job information"""
    job_info: JobInfo
    job_flags: JobFlags
    plugin: JobPlugin
    alerts: JobAlerts
    servers: list

@dataclass
class ServerSchedule:
    """Server schedule"""
    sunday: int
    monday: int
    tuesday: int
    wednesday: int
    thursday: int
    friday: int
    saturday: int

@dataclass
class ServerListItem:
    """Server item in list"""
    handle: str
    state: int
    name: str

@dataclass 
class Server:
    """Server information"""
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
