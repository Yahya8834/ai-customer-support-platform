class BusinessLogicError(Exception):
    """Raised when a business rule is violated."""
    pass


class AlreadyWorkspaceMemberError(BusinessLogicError):
    """Raised when a user is already a member of the workspace."""
    pass


class WorkspaceNotFoundError(Exception):
    """Raised when a workspace is not found."""
    pass


class DocumentNotFoundError(Exception):
    """Raised when a document is not found."""
    pass


class EmbeddingGenerationError(Exception):
    """Raised when there is an error generating embeddings."""
    pass


class AIServiceError(Exception):
    """Raised when communication with the AI service fails."""