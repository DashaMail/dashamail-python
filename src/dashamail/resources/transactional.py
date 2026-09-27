from urllib.parse import quote

from .base import BaseResource


class Transactional(BaseResource):
    """
    One-off transactional emails: send, status, log, stats.
    Requires a verified sending domain — see Account.add_domain().
    https://dashamail.ru/api/transactional/
    """

    def send(self, to, from_email, message, **params):
        """
        POST /transactional/messages

        :param to: A single address, or a list of addresses/objects.
        :param from_email: Verified sending address.
        :param message: HTML body.
        :param params: from_name, subject, plain_text, message_id, cc, bcc, headers,
                        attachments, inline, delivery_time, domain, stat_domain...
        """
        params["to"] = to
        params["from_email"] = from_email
        params["message"] = message
        return self._client.request("POST", "/transactional/messages", None, params)

    def check(self, transaction_id):
        """GET /transactional/messages/{transaction_id} — delivery status of one message."""
        return self._client.request("GET", "/transactional/messages/{}".format(quote(transaction_id, safe="")))

    def log(self, **params):
        """GET /transactional/log"""
        return self._client.request("GET", "/transactional/log", params)

    def stats(self, **params):
        """GET /transactional/stats"""
        return self._client.request("GET", "/transactional/stats", params)
