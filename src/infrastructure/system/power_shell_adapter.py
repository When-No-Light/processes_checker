import json
import subprocess

from domain.value_objects import Metadata, ProcessesInfoSnapshot
from utils.dt import get_utcdt_and_local_timezone


class PowerShellAdapter:
    """Class for operations with specific power shell."""

    def __init__(self):
        self.power_shell = (
            "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe"
        )

    def get_processes_info(self) -> ProcessesInfoSnapshot:

        get_whole_processes_json_command = "Get-Process | Select-Object Handles, \
            NPM, PM, WS, CPU, Id, SI, ProcessName | ConvertTo-Json  -Compress"
        result = subprocess.run(
            [self.power_shell, get_whole_processes_json_command],
            capture_output=True,
            text=True,
            shell=True,
            check=False,
        )
        json_output = result.stdout.strip()
        created_at_utc, tzname = get_utcdt_and_local_timezone()
        processes_info_snapshot = ProcessesInfoSnapshot(
            processes_info=json.loads(json_output),
            metadata=Metadata(created_at_utc=created_at_utc, tzname=tzname),
        )
        return processes_info_snapshot

    def get_mac_address(self) -> str:
        get_mac_address_command = "Get-WmiObject -Class Win32_NetworkAdapterConfiguration | \
            Where-Object {$_.IPEnabled -eq $true} | Select-Object -ExpandProperty MACAddress"
        result = subprocess.run(
            [self.power_shell, get_mac_address_command],
            capture_output=True,
            text=True,
            shell=True,
            check=False,
        )

        return result.stdout.strip()

    def get_computer_name(self) -> str:
        get_computer_name_str_command = "$env:COMPUTERNAME"
        result = subprocess.run(
            [self.power_shell, get_computer_name_str_command],
            capture_output=True,
            text=True,
            shell=True,
            check=False,
        )

        return result.stdout.strip()
