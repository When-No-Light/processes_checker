import subprocess
import json
from typing import List
from typing import TypedDict, Optional

class ProcessInfo(TypedDict, total=False):
    Handles: int
    NPM: int
    PM: Optional[int]  # Email is optional
    WS: Optional[int]  # Email is optional
    CPU: Optional[float]  # Email is optional
    Id: Optional[int]  # Email is optional
    SI: Optional[int]  # Email is optional
    ProcessName: Optional[str]  # Email is optional


class PowerShellAdapter:
    """Class for operations with specific power shell."""

    def __init__(self):
        self.power_shell = 'C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe'


    def get_processes_json(self) -> List[ProcessInfo]:
        
        get_whole_processes_json = 'Get-Process | Select-Object Handles, NPM, PM, WS, CPU, Id, SI, ProcessName | ConvertTo-Json  -Compress'
        result = subprocess.run(
            [self.power_shell, get_whole_processes_json],
            capture_output=True,
            text=True,
            shell=True
        )
        json_output = result.stdout.strip()

        return json.loads(json_output)
