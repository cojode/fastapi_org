class RepositoryError(Exception):
    """Repository layer related error."""


class DomainError(Exception):
    """Domain layer related error."""


class NotFoundError(DomainError):
    """Singular enitity expected but not found error."""
