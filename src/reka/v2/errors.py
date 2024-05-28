"""Reka-specific exceptions."""

from typing import Optional


class RekaError(Exception):
    """Something wrong happened with the request."""

    def __init__(
        self, underlying: Optional[Exception] = None, reason: Optional[str] = None
    ) -> None:
        self.underlying = underlying
        self.reason = reason
        super().__init__()

    def __str__(self) -> str:
        return repr(self)

    def __repr__(self) -> str:
        properties = []
        if self.underlying is not None:
            properties.append(f"Underlying={self.underlying}")
        if self.reason is not None:
            properties.append(f"Reason={self.reason}")
        properties_str = ", ".join(properties)

        repr_str = f"{self.__class__.__name__}"
        if properties_str:
            repr_str += f": {properties_str}"

        return repr_str


class DatasetError(RekaError):
    """Something wrong with processing datasets"""

    ...


class RetrievalError(RekaError):
    """Something wrong with retrieval"""

    ...


class AuthError(RekaError, ValueError): ...


class InvalidConversationError(RekaError): ...
