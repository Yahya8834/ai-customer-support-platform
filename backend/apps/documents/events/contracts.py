from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class DocumentUploadedEvent:
    """
    Domain event emitted after a document has been successfully uploaded.
    """
    
    document_uuid: UUID
    workspace_uuid: UUID
    uploaded_by_uuid: UUID