from mongoengine import connect

from domain.entities import ComputerMonitoringHistory
from domain.value_objects import ProcessesInfoSnapshot
from infrastructure.repository.models import (
    ComputerMonitoringHistoryDocument,
    ProcessesInfoSnapshotDocument,
)


class MongoDbAdapter:
    def __init__(self):
        self._computer_monitoring_history_doc = None
        connect(
            db="mydatabase",
            host="localhost",
            port=27017,
            username="root",
            password="example",
            # authentication_source="admin",  # Required for root user
        )

    def get_computer_history(self, mac_address: str) -> ComputerMonitoringHistory:
        """Returns computer processes log story."""
        try:
            computer_monitoring_history_doc = ComputerMonitoringHistoryDocument.objects(
                mac_address=mac_address
            )
            if not isinstance(
                computer_monitoring_history_doc, ComputerMonitoringHistoryDocument
            ):
                raise ValueError
            return computer_monitoring_history_doc.to_domain()
        except AttributeError:  # TODO check
            return None

    def add_computer_story_if_not_exist(
        self, computer_monitoring_history: ComputerMonitoringHistory
    ) -> None:

        try:
            self._computer_monitoring_history_doc = ComputerMonitoringHistoryDocument.objects.get(  # pylint: disable=no-member
                mac_address=computer_monitoring_history.mac_address
            )

        except (
            ComputerMonitoringHistoryDocument.DoesNotExist  # pylint: disable=no-member
        ):
            self._computer_monitoring_history_doc = (
                ComputerMonitoringHistoryDocument.from_domain(
                    computer_monitoring_history
                )
            )
            self._computer_monitoring_history_doc.save()

    def add_processes_info_snapshot_to_history(
        self, processes_info_snapshot: ProcessesInfoSnapshot
    ) -> None:

        if not isinstance(
            self._computer_monitoring_history_doc, ComputerMonitoringHistoryDocument
        ):
            raise ValueError("computer_monitoring_history_doc wa not set")

        processes_info_snapshot_doc = ProcessesInfoSnapshotDocument.from_domain(
            processes_info_snapshot
        )

        self._computer_monitoring_history_doc.processes_info_snapshots.create(
            processes_info=processes_info_snapshot_doc.processes_info,
            metadata=processes_info_snapshot_doc.metadata,
        )
        # a = self._computer_monitoring_history_doc.processes_info_snapshots[4].to_domain()
        self._computer_monitoring_history_doc.save()
