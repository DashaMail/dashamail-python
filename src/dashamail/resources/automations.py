from .base import BaseResource


class Automations(BaseResource):
    """
    Event-triggered emails (subscribe, add, open, click, field change...).
    https://dashamail.ru/api/automations/
    """

    def events(self):
        """GET /automations/events — reference of available trigger events."""
        return self._client.request("GET", "/automations/events")

    def all(self, **params):
        """GET /automations"""
        return self._client.request("GET", "/automations", params)

    def create(self, **params):
        """POST /automations — requires list_id, subject, from_email, from_name; see the API docs for the rest."""
        return self._client.request("POST", "/automations", None, params)

    def update(self, campaign_id, **params):
        """PUT /automations/{campaign_id}"""
        return self._client.request("PUT", "/automations/{}".format(campaign_id), None, params)

    def delete(self, campaign_id):
        """DELETE /automations/{campaign_id}"""
        return self._client.request("DELETE", "/automations/{}".format(campaign_id))

    def trigger(self, campaign_id, email, **params):
        """POST /automations/{campaign_id}/trigger — force-run for one subscriber (fails with code 37 before moderation)."""
        params["email"] = email
        return self._client.request("POST", "/automations/{}/trigger".format(campaign_id), None, params)
