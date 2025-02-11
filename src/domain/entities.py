from dataclasses import dataclass
from typing import List

from domain.value_objects import ProcessesInfoSnapshot


@dataclass
class ComputerMonitoringHistory:

    processes_info_snapshots: List[ProcessesInfoSnapshot]
    mac_address: str
    computer_name: str
