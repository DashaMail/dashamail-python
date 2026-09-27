import base64

from .base import BaseResource


class Images(BaseResource):
    """
    Resize (>1600px wide) and recompress an image the same way DashaMail's own
    file manager does, without changing its format or storing anything.
    https://dashamail.ru/api/images/
    """

    def optimize(self, binary_data, **params):
        """
        Optimize an image already loaded in memory (JSON body, base64-encoded).

        :param binary_data: Raw image bytes (JPEG/PNG/GIF).
        :param params: resize (bool, default True), max_width (int), lossy (bool).
        :return: Response whose data["image"] is the base64-encoded result.
        """
        params["image"] = base64.b64encode(binary_data).decode("ascii")
        return self._client.request("POST", "/images/optimize", None, params)

    def optimize_file(self, file_path, **params):
        """
        Optimize an image already sitting on disk, uploaded as multipart/form-data.

        :return: Response whose data["image"] is the base64-encoded result.
        """
        return self._client.request_multipart("POST", "/images/optimize", None, params, "file", file_path)

    def optimize_file_binary(self, file_path, **params):
        """Same as optimize_file(), but returns raw optimized bytes (?response=binary)."""
        return self._client.request_multipart_binary(
            "POST", "/images/optimize", {"response": "binary"}, params, "file", file_path
        )

    def optimize_binary(self, binary_data, **params):
        """Same as optimize(), but returns raw optimized bytes (?response=binary)."""
        params["image"] = base64.b64encode(binary_data).decode("ascii")
        return self._client.request_binary("POST", "/images/optimize", {"response": "binary"}, params)
