import json

from dashamail.client import Client


class FakeClient(Client):
    """
    A Client that never touches the network: _execute() is stubbed to return
    a canned HTTP response queued up front, so resource classes can be
    tested against realistic API payloads.
    """

    def __init__(self, api_key="test-key", **kwargs):
        super().__init__(api_key, **kwargs)
        self._queue = []
        self.calls = []

    def queue_response(self, status, decoded_body_or_raw, headers=None):
        if isinstance(decoded_body_or_raw, (bytes, str)):
            body = decoded_body_or_raw
            if isinstance(body, str):
                body = body.encode("utf-8")
        else:
            body = json.dumps(decoded_body_or_raw, ensure_ascii=False).encode("utf-8")
        self._queue.append((status, body, headers or {}))
        return self

    def _execute(self, method, url, headers, data):
        self.calls.append({"method": method, "url": url, "headers": headers, "data": data})
        if not self._queue:
            raise RuntimeError("FakeClient: no queued response for {} {}".format(method, url))
        return self._queue.pop(0)
