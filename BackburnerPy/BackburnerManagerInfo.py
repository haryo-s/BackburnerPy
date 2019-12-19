from dataclasses import dataclass
from NetworkStatus import NetworkStatus
from SystemInfo import SystemInfo

@dataclass
class BackBurnerManagerInfo:
    version: int
    servers: int
    jobs: int
    system_info: SystemInfo
    network_status: NetworkStatus
