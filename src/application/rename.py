import time

from domain.entities import ComputerMonitoringHistory
from infrastructure.repository.adapter import MongoDbAdapter
from infrastructure.system.power_shell_adapter import PowerShellAdapter


class ComputerMonitoringManager:

    def __init__(self):
        self._system_adapter = PowerShellAdapter()
        self._repository = MongoDbAdapter()
        self._mac_address = self._system_adapter.get_mac_address()

    def _init_computer_history(self):
        """Init ComputerMonitoringHistory if it doesn't exist."""

        computer_monitoring_history = ComputerMonitoringHistory(
            computer_name=self._system_adapter.get_computer_name(),
            mac_address=self._mac_address,
            processes_info_snapshots=[],
        )
        self._repository.add_computer_story_if_not_exist(
            computer_monitoring_history=computer_monitoring_history
        )

    def _write_processes_snapshot(self):

        processes_info_snapshot = self._system_adapter.get_processes_info()
        self._repository.add_processes_info_snapshot_to_history(
            processes_info_snapshot=processes_info_snapshot
        )

    # TODO add signal handler  to write to db exit code and time

    def _run_process_watcher(self):

        self._init_computer_history()

        while True:
            self._write_processes_snapshot()
            time.sleep(10)  # TODO from config

    def start_monitoring(self):

        self._run_process_watcher()
