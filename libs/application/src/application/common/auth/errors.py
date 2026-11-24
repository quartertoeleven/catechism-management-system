"""Authentication errors."""


class AuthenticationError(Exception):
    """Raised when an authentication operation fails."""


class CatechistLinkError(AuthenticationError):
    """Raised when the authenticated user is not linked to a catechist."""
