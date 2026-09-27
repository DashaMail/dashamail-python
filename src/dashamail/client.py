"""Thin HTTP layer over the DashaMail REST API v2 (https://dashamail.ru/api/)."""

import json
import mimetypes
import os
import uuid
import urllib.error
import urllib.parse
import urllib.request

from .binary_response import BinaryResponse
from .exceptions import ApiException, NetworkException
from .response import Response

DEFAULT_BASE_URL = "https://api.dashamail.com/v2"
VERSION = "1.0.0"


class Client:
    """
    Talks JSON over ``urllib`` with no third-party dependencies. Resource
    classes (``dashamail.resources.*``) build on top of request()/
    request_multipart(); most applications should go through
    ``dashamail.DashaMail`` rather than use this class directly.
    """

    def __init__(self, api_key, base_url=None, timeout=30, user_agent=None):
        """
        :param api_key: Account API key — Личный кабинет → Аккаунт → API и интеграции.
        :param base_url: Override the API origin, e.g. for a proxy or a mock server.
        :param timeout: Request timeout in seconds. Default 30.
        :param user_agent: Override the User-Agent header.
        """
        if not isinstance(api_key, str) or not api_key:
            raise ValueError("DashaMail API key must be a non-empty string.")
        self.api_key = api_key
        self.base_url = (base_url or DEFAULT_BASE_URL).rstrip("/")
        self.timeout = timeout
        self.user_agent = user_agent or "dashamail-python/{}".format(VERSION)

    def request(self, method, path, query=None, body=None):
        """
        JSON request. Body is sent as ``application/json``; on 2xx the
        decoded ``response.data`` is returned wrapped in a Response, on
        error an ApiException subclass is raised.

        :return: Response, or None for a 204 No Content.
        """
        url = self._build_url(path, query)
        headers = self._base_headers()
        data = None
        if body is not None:
            data = json.dumps(body, ensure_ascii=False).encode("utf-8")
            headers["Content-Type"] = "application/json"

        status, raw_body, resp_headers = self._execute(method.upper(), url, headers, data)
        return self._parse_json_response(status, raw_body, resp_headers)

    def request_multipart(self, method, path, query, fields, file_field, file_path, file_name=None, mime_type=None):
        """multipart/form-data request with a single file field — used by POST /images/optimize."""
        body, content_type = self._build_multipart(fields, file_field, file_path, file_name, mime_type)
        url = self._build_url(path, query)
        headers = self._base_headers()
        headers["Content-Type"] = content_type

        status, raw_body, resp_headers = self._execute(method.upper(), url, headers, body)
        return self._parse_json_response(status, raw_body, resp_headers)

    def request_multipart_binary(self, method, path, query, fields, file_field, file_path, file_name=None, mime_type=None):
        """Same as request_multipart(), but returns raw bytes instead of decoding JSON."""
        body, content_type = self._build_multipart(fields, file_field, file_path, file_name, mime_type)
        url = self._build_url(path, query)
        headers = self._base_headers()
        headers["Content-Type"] = content_type

        status, raw_body, resp_headers = self._execute(method.upper(), url, headers, body)
        return self._parse_binary_response(status, raw_body, resp_headers)

    def request_binary(self, method, path, query=None, body=None):
        """Same as request(), but returns raw bytes instead of decoding JSON."""
        url = self._build_url(path, query)
        headers = self._base_headers()
        data = None
        if body is not None:
            data = json.dumps(body, ensure_ascii=False).encode("utf-8")
            headers["Content-Type"] = "application/json"

        status, raw_body, resp_headers = self._execute(method.upper(), url, headers, data)
        return self._parse_binary_response(status, raw_body, resp_headers)

    def _base_headers(self):
        return {
            "Authorization": "Bearer {}".format(self.api_key),
            "Accept": "application/json",
            "User-Agent": self.user_agent,
        }

    def _build_url(self, path, query):
        url = self.base_url + "/" + path.lstrip("/")
        if query:
            filtered = {k: v for k, v in query.items() if v is not None}
            if filtered:
                url += "?" + urllib.parse.urlencode(filtered)
        return url

    def _build_multipart(self, fields, file_field, file_path, file_name, mime_type):
        if not os.path.isfile(file_path) or not os.access(file_path, os.R_OK):
            raise ValueError("File not readable: {}".format(file_path))
        file_name = file_name or os.path.basename(file_path)
        mime_type = mime_type or mimetypes.guess_type(file_path)[0] or "application/octet-stream"
        with open(file_path, "rb") as fh:
            file_content = fh.read()

        boundary = uuid.uuid4().hex
        parts = []
        for key, value in (fields or {}).items():
            parts.append("--{}\r\n".format(boundary).encode("utf-8"))
            parts.append('Content-Disposition: form-data; name="{}"\r\n\r\n'.format(key).encode("utf-8"))
            parts.append(str(value).encode("utf-8"))
            parts.append(b"\r\n")
        parts.append("--{}\r\n".format(boundary).encode("utf-8"))
        parts.append(
            'Content-Disposition: form-data; name="{}"; filename="{}"\r\n'.format(file_field, file_name).encode("utf-8")
        )
        parts.append("Content-Type: {}\r\n\r\n".format(mime_type).encode("utf-8"))
        parts.append(file_content)
        parts.append(b"\r\n")
        parts.append("--{}--\r\n".format(boundary).encode("utf-8"))

        return b"".join(parts), "multipart/form-data; boundary={}".format(boundary)

    def _parse_json_response(self, status, raw_body, headers):
        if status == 204 or not raw_body:
            return None

        try:
            decoded = json.loads(raw_body.decode("utf-8"))
        except (ValueError, UnicodeDecodeError) as exc:
            raise NetworkException(
                "DashaMail API returned a non-JSON response (HTTP {}): {}".format(
                    status, raw_body[:500]
                )
            ) from exc

        if 200 <= status < 300:
            response = decoded.get("response", decoded) if isinstance(decoded, dict) else decoded
            if isinstance(response, dict) and "data" in response:
                data = response["data"]
            else:
                data = response
            message = None
            if isinstance(response, dict) and isinstance(response.get("msg"), dict):
                message = response["msg"].get("text")
            meta = decoded.get("meta") if isinstance(decoded, dict) and isinstance(decoded.get("meta"), dict) else {}
            return Response(data, meta, message)

        error = decoded.get("error") if isinstance(decoded, dict) else None
        raise ApiException.from_error(status, error or {"code": status, "message": "Unknown DashaMail API error"})

    def _parse_binary_response(self, status, raw_body, headers):
        if 200 <= status < 300:
            content_type = headers.get("Content-Type") or headers.get("content-type") or "application/octet-stream"
            return BinaryResponse(raw_body, content_type, status)

        try:
            decoded = json.loads(raw_body.decode("utf-8"))
        except (ValueError, UnicodeDecodeError):
            decoded = {}
        error = decoded.get("error") if isinstance(decoded, dict) else None
        raise ApiException.from_error(status, error or {"code": status, "message": "Unknown DashaMail API error"})

    def _execute(self, method, url, headers, data):
        """
        Low-level HTTP call. Kept as its own method so tests can stub it out
        without a real network connection — subclass Client and override
        _execute().

        :return: (status, raw_body: bytes, headers: dict)
        """
        request = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as resp:
                return resp.status, resp.read(), dict(resp.headers.items())
        except urllib.error.HTTPError as exc:
            body = exc.read()
            resp_headers = dict(exc.headers.items()) if exc.headers else {}
            return exc.code, body, resp_headers
        except urllib.error.URLError as exc:
            raise NetworkException("Network error: {}".format(exc.reason)) from exc
        except OSError as exc:
            raise NetworkException("Network error: {}".format(exc)) from exc
