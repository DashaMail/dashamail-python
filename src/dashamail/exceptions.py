"""Exceptions raised by the DashaMail SDK."""


class ApiException(Exception):
    """
    Raised for any error response from the DashaMail API (HTTP status >= 400
    with a JSON {"error": {"code", "message", "details"}} body).

    The HTTP status and DashaMail's own error ``code`` are different numbers:
    ``code`` is stable across API versions and documented at
    https://dashamail.ru/api/errors/, while the HTTP status is a coarser
    REST-ification of it.
    """

    def __init__(self, message, http_status, api_code=0, details=None):
        super().__init__(message)
        self.http_status = http_status
        self.api_code = api_code
        self.details = details or {}

    @classmethod
    def from_error(cls, http_status, error):
        """Build the most specific exception subclass for a given HTTP status."""
        error = error if isinstance(error, dict) else {}
        message = str(error.get("message") or "DashaMail API error")
        try:
            api_code = int(error.get("code", http_status))
        except (TypeError, ValueError):
            api_code = http_status
        details = error.get("details") if isinstance(error.get("details"), dict) else {}

        exc_cls = _STATUS_TO_EXCEPTION.get(int(http_status))
        if exc_cls is None:
            exc_cls = ServerException if http_status >= 500 else cls
        return exc_cls(message, http_status, api_code, details)


class AuthenticationException(ApiException):
    """HTTP 401 — missing or invalid API key."""


class PaymentRequiredException(ApiException):
    """HTTP 402 — the account's balance or plan does not allow this action."""


class AuthorizationException(ApiException):
    """HTTP 403 — the API key is valid but lacks the rights or scope for this action."""


class NotFoundException(ApiException):
    """HTTP 404 — the resource (or the account itself) does not exist."""


class ConflictException(ApiException):
    """HTTP 409 — the request conflicts with the resource's current state."""


class PayloadTooLargeException(ApiException):
    """HTTP 413 — the uploaded file or attachment is too large."""


class ValidationException(ApiException):
    """HTTP 422 — a required field is missing or a value is invalid."""


class RateLimitException(ApiException):
    """HTTP 429 — too many requests. See get_retry_after() for how long to back off."""

    def get_retry_after(self):
        value = self.details.get("retry_after")
        return int(value) if value is not None else None


class ServerException(ApiException):
    """HTTP 5xx — something failed on DashaMail's side. Usually safe to retry."""


class NetworkException(Exception):
    """The request never got an HTTP response (DNS, TLS, timeout, connection reset...)."""


_STATUS_TO_EXCEPTION = {
    401: AuthenticationException,
    402: PaymentRequiredException,
    403: AuthorizationException,
    404: NotFoundException,
    409: ConflictException,
    413: PayloadTooLargeException,
    422: ValidationException,
    429: RateLimitException,
}
