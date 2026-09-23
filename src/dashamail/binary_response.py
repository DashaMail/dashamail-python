"""Raw-bytes response for the one endpoint that can answer outside JSON."""


class BinaryResponse:
    """
    Raw bytes returned by an endpoint that can answer outside JSON —
    currently only ``POST /images/optimize?response=binary``.
    """

    def __init__(self, body, content_type, http_status):
        self.body = body
        self.content_type = content_type
        self.http_status = http_status

    def save_to(self, path):
        """Write the bytes to a file. Returns the number of bytes written."""
        with open(path, "wb") as fh:
            return fh.write(self.body)
