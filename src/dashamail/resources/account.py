from urllib.parse import quote

from .base import BaseResource


class Account(BaseResource):
    """
    Account balance and limits, confirmed senders, sending domains, webhooks.
    https://dashamail.ru/api/account/
    """

    def balance(self):
        """GET /account/balance"""
        return self._client.request("GET", "/account/balance")

    def senders(self):
        """GET /account/senders — confirmed From: addresses."""
        return self._client.request("GET", "/account/senders")

    def confirm_sender(self, email, code):
        """POST /account/senders/confirm — confirm a sender address with the code emailed to it."""
        return self._client.request("POST", "/account/senders/confirm", None, {"email": email, "code": code})

    def domains(self, **params):
        """GET /account/domains — sending domains."""
        return self._client.request("GET", "/account/domains", params)

    def add_domain(self, domain, **params):
        """POST /account/domains — add a sending domain."""
        params["domain"] = domain
        return self._client.request("POST", "/account/domains", None, params)

    def check_domains(self, **params):
        """GET /account/domains/check — check DNS (DKIM/SPF) validity of sending domains."""
        return self._client.request("GET", "/account/domains/check", params)

    def delete_domain(self, domain, **params):
        """DELETE /account/domains/{domain}"""
        return self._client.request("DELETE", "/account/domains/{}".format(quote(domain, safe="")), None, params)

    def webhooks(self, **params):
        """GET /account/webhooks — bulk-campaign webhooks."""
        return self._client.request("GET", "/account/webhooks", params)

    def add_webhook(self, event, url, **params):
        """POST /account/webhooks — event is one of: open, click, hard, spam, unsub, subscribe, confirm."""
        params["event"] = event
        params["url"] = url
        return self._client.request("POST", "/account/webhooks", None, params)

    def delete_webhook(self, event_name):
        """DELETE /account/webhooks/{event_name}"""
        return self._client.request("DELETE", "/account/webhooks/{}".format(quote(event_name, safe="")))

    def transactional_webhooks(self, **params):
        """GET /account/webhooks/transactional"""
        return self._client.request("GET", "/account/webhooks/transactional", params)

    def add_transactional_webhook(self, event, url, **params):
        """POST /account/webhooks/transactional — event is one of: send, delivered, dropped, open, click, hard, spam, unsub."""
        params["event"] = event
        params["url"] = url
        return self._client.request("POST", "/account/webhooks/transactional", None, params)

    def delete_transactional_webhook(self, event_name):
        """DELETE /account/webhooks/transactional/{event_name}"""
        return self._client.request(
            "DELETE", "/account/webhooks/transactional/{}".format(quote(event_name, safe=""))
        )
