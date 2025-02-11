from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, TypedDict


class ProcessInfo(TypedDict, total=False):
    Handles: int  # Number of handles opened by the process
    NPM: int  # Non-paged memory size used by the process
    PM: Optional[int]  # Paged memory size (optional)
    WS: Optional[int]  # Working set size (optional)
    CPU: Optional[float]  # CPU usage percentage (optional)
    Id: Optional[int]  # Process ID (optional)
    SI: Optional[int]  # Session ID (optional)
    ProcessName: Optional[str]  # Name of the process (optional)


@dataclass
class Metadata:
    created_at_utc: datetime
    tzname: str


@dataclass
class ProcessesInfoSnapshot:

    processes_info: List[ProcessInfo]
    metadata: Metadata
