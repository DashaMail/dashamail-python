from .base import BaseResource


class Dialogs(BaseResource):
    """
    Subscriber replies to campaigns, threaded per subscriber.
    https://dashamail.ru/api/dialogs/
    """

    def all(self, **params):
        """GET /dialogs"""
        return self._client.request("GET", "/dialogs", params)

    def get(self, dialog_id):
        """GET /dialogs/{dialog_id}"""
        return self._client.request("GET", "/dialogs/{}".format(dialog_id))

    def messages(self, dialog_id, **params):
        """GET /dialogs/{dialog_id}/messages"""
        return self._client.request("GET", "/dialogs/{}/messages".format(dialog_id), params)

    def reply(self, dialog_id, body_text, **params):
        """POST /dialogs/{dialog_id}/reply — reply as the campaign's sender."""
        params["body_text"] = body_text
        return self._client.request("POST", "/dialogs/{}/reply".format(dialog_id), None, params)

    def mark_read(self, dialog_id, **params):
        """POST /dialogs/{dialog_id}/read"""
        return self._client.request("POST", "/dialogs/{}/read".format(dialog_id), None, params)

    def mark_unread(self, dialog_id):
        """POST /dialogs/{dialog_id}/unread"""
        return self._client.request("POST", "/dialogs/{}/unread".format(dialog_id))

    def close(self, dialog_id):
        """POST /dialogs/{dialog_id}/close"""
        return self._client.request("POST", "/dialogs/{}/close".format(dialog_id))

    def open(self, dialog_id):
        """POST /dialogs/{dialog_id}/open"""
        return self._client.request("POST", "/dialogs/{}/open".format(dialog_id))

    def unread_count(self):
        """GET /dialogs/unread-count"""
        return self._client.request("GET", "/dialogs/unread-count")

    def attachment(self, attachment_id):
        """GET /dialogs/attachments/{attachment_id} — link to a reply's attachment."""
        return self._client.request("GET", "/dialogs/attachments/{}".format(attachment_id))
