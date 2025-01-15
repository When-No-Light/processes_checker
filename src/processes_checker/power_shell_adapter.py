import subprocess
import json
from typing import List
from typing import TypedDict, Optional

class ProcessInfo(TypedDict, total=False):
    Handles: int  # Number of handles opened by the process
    NPM: int  # Non-paged memory size used by the process
    PM: Optional[int]  # Paged memory size (optional)
    WS: Optional[int]  # Working set size (optional)
    CPU: Optional[float]  # CPU usage percentage (optional)
    Id: Optional[int]  # Process ID (optional)
    SI: Optional[int]  # Session ID (optional)
    ProcessName: Optional[str]  # Name of the process (optional)

# Define a class to handle operations involving PowerShell
class PowerShellAdapter:
    """Class for operations with specific PowerShell commands."""

    def __init__(self):
        self.power_shell = 'C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe'


    def get_processes_json(self) -> List[ProcessInfo]:
        """
        Fetches a list of processes and their details from PowerShell as JSON.

        Returns:
            List[ProcessInfo]: A list of dictionaries containing process information.
        """
        # PowerShell command to retrieve process details and convert them to JSON
        get_whole_processes_json = (
            'Get-Process | Select-Object Handles, NPM, PM, WS, CPU, Id, SI, ProcessName | ConvertTo-Json -Compress'
        )
        
        # Execute the PowerShell command using subprocess
        result = subprocess.run(
            [self.power_shell, get_whole_processes_json],
            capture_output=True,
            text=True,
            shell=True
        )
        json_output = result.stdout.strip()

        return json.loads(json_output)
