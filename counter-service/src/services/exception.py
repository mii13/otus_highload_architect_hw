class BaseServiceException(Exception):
    """base service exception."""


class TypeNotFoundException(BaseServiceException):
    """raise if type not found."""
