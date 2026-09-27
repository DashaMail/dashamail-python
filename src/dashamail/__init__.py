"""Official Python SDK for the DashaMail REST API v2 (https://dashamail.ru/api/)."""

from .client import Client
from .dashamail import DashaMail
from .binary_response import BinaryResponse
from .response import Response
from .exceptions import (
    ApiException,
    AuthenticationException,
    AuthorizationException,
    ConflictException,
    NetworkException,
    NotFoundException,
    PaymentRequiredException,
    PayloadTooLargeException,
    RateLimitException,
    ServerException,
    ValidationException,
)

__version__ = "1.0.0"

__all__ = [
    "DashaMail",
    "Client",
    "Response",
    "BinaryResponse",
    "ApiException",
    "AuthenticationException",
    "AuthorizationException",
    "ConflictException",
    "NetworkException",
    "NotFoundException",
    "PaymentRequiredException",
    "PayloadTooLargeException",
    "RateLimitException",
    "ServerException",
    "ValidationException",
]
