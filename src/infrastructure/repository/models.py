from mongoengine import (
    DateTimeField,
    Document,
    EmbeddedDocument,
    EmbeddedDocumentField,
    EmbeddedDocumentListField,
    FloatField,
    IntField,
    StringField,
)

from domain.entities import ComputerMonitoringHistory, ProcessesInfoSnapshot
from domain.value_objects import Metadata, ProcessInfo


class ProcessInfoDocument(EmbeddedDocument):
    """Represents a document schema for process information within a MongoDB collection."""

    Handles = IntField(required=True)
    NPM = IntField(required=True)
    PM = IntField(required=False)
    WS = IntField(required=False)
    CPU = FloatField(required=False)
    Id = IntField(required=False)
    SI = IntField(required=False)
    ProcessName = StringField(required=False)

    def to_domain(self) -> ProcessInfo:
        """Convert the ProcessInfoDocument to a ProcessInfo domain object."""

        return ProcessInfo(
            Handles=self.Handles,
            NPM=self.NPM,
            PM=self.PM,
            WS=self.WS,
            CPU=self.CPU,
            Id=self.Id,
            SI=self.SI,
            ProcessName=self.ProcessName,
        )

    @classmethod
    def from_domain(cls, process_info: ProcessInfo) -> "ProcessInfoDocument":
        """Create a ProcessInfoDocument from a ProcessInfo domain object."""

        return cls(
            Handles=process_info["Handles"],
            NPM=process_info["NPM"],
            PM=process_info["PM"],
            WS=process_info["WS"],
            CPU=process_info["CPU"],
            Id=process_info["Id"],
            SI=process_info["SI"],
            ProcessName=process_info["ProcessName"],
        )


class MetadataDocument(EmbeddedDocument):
    """Represents metadata for a snapshot of process information."""

    created_at_utc = DateTimeField(required=True)
    tzname = StringField(required=True)

    def to_domain(self) -> Metadata:
        """Convert the MetadataDocument to a Metadata domain object."""

        return Metadata(
            created_at_utc=self.created_at_utc,
            tzname=self.tzname,
        )

    @classmethod
    def from_domain(cls, metadata: Metadata) -> "MetadataDocument":
        """Create a MetadataDocument from a Metadata domain object."""

        return cls(
            created_at_utc=metadata.created_at_utc,
            tzname=metadata.tzname,
        )


class ProcessesInfoSnapshotDocument(EmbeddedDocument):

    processes_info = EmbeddedDocumentListField(ProcessInfoDocument)
    metadata = EmbeddedDocumentField(MetadataDocument, required=True)

    def to_domain(self) -> ProcessesInfoSnapshot:

        return ProcessesInfoSnapshot(
            processes_info=[
                _embeded_document_to_domain(process_info)
                for process_info in self.processes_info
            ],
            metadata=_embeded_document_to_domain(self.metadata),
        )

    @classmethod
    def from_domain(
        cls, processes_info_snapshot: ProcessesInfoSnapshot
    ) -> "ProcessesInfoSnapshotDocument":

        return cls(
            processes_info=[
                ProcessInfoDocument.from_domain(process_info)
                for process_info in processes_info_snapshot.processes_info
            ],
            metadata=MetadataDocument.from_domain(processes_info_snapshot.metadata),
        )


class ComputerMonitoringHistoryDocument(Document):

    processes_info_snapshots = EmbeddedDocumentListField(ProcessesInfoSnapshotDocument)
    mac_address = StringField(primary_key=True)
    computer_name = StringField(required=True)

    def to_domain(self) -> ComputerMonitoringHistory:
        return ComputerMonitoringHistory(
            processes_info_snapshots=[
                _embeded_document_to_domain(snapshot)
                for snapshot in self.processes_info_snapshots
            ],
            mac_address=self.mac_address,
            computer_name=self.computer_name,
        )

    @classmethod
    def from_domain(
        cls, computer_monitoring_history: ComputerMonitoringHistory
    ) -> "ComputerMonitoringHistoryDocument":

        return cls(
            processes_info_snapshots=[
                ProcessesInfoSnapshotDocument.from_domain(snapshot)
                for snapshot in computer_monitoring_history.processes_info_snapshots
            ],
            mac_address=computer_monitoring_history.mac_address,
            computer_name=computer_monitoring_history.computer_name,
        )


def _embeded_document_to_domain(embeded_document: EmbeddedDocument):

    if not isinstance(
        embeded_document,
        (ProcessInfoDocument, MetadataDocument, ProcessesInfoSnapshotDocument),
    ):
        raise ValueError("Embeded document type is not as expected!")

    return embeded_document.to_domain()
