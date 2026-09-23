from .base import BaseResource


class Segments(BaseResource):
    """
    Saved subscriber segments: condition sets, field/operator reference, size counting.
    https://dashamail.ru/api/segments/
    """

    def all(self, **params):
        """GET /segments"""
        return self._client.request("GET", "/segments", params)

    def get(self, segment_id):
        """GET /segments/{segment_id}"""
        return self._client.request("GET", "/segments/{}".format(segment_id))

    def create(self, list_id, name, esegment, **params):
        """POST /segments — esegment is a condition tree, e.g. {"match": "all", "c": [...]}."""
        params["list_id"] = list_id
        params["name"] = name
        params["esegment"] = esegment
        return self._client.request("POST", "/segments", None, params)

    def update(self, segment_id, **params):
        """PUT /segments/{segment_id}"""
        return self._client.request("PUT", "/segments/{}".format(segment_id), None, params)

    def delete(self, segment_id):
        """DELETE /segments/{segment_id}"""
        return self._client.request("DELETE", "/segments/{}".format(segment_id))

    def count(self, **params):
        """POST /segments/count — recompute a segment's size, by id or by passing list_id + esegment directly."""
        return self._client.request("POST", "/segments/count", None, params)

    def fields(self, list_id):
        """GET /segments/fields — which fields/operators are available for a list's segments."""
        return self._client.request("GET", "/segments/fields", {"list_id": list_id})
