from .base import BaseResource


class Workflows(BaseResource):
    """
    Visual-builder automation scenarios.
    https://dashamail.ru/api/automations/#workflows
    """

    def all(self):
        """GET /workflows"""
        return self._client.request("GET", "/workflows")

    def get(self, workflow_id):
        """GET /workflows/{workflow_id}"""
        return self._client.request("GET", "/workflows/{}".format(workflow_id))

    def delete(self, workflow_id):
        """DELETE /workflows/{workflow_id}"""
        return self._client.request("DELETE", "/workflows/{}".format(workflow_id))

    def copy(self, workflow_id, **params):
        """POST /workflows/{workflow_id}/copy"""
        return self._client.request("POST", "/workflows/{}/copy".format(workflow_id), None, params)
