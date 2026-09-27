from .base import BaseResource


class Router(BaseResource):
    """
    Inbound mail processing: receiving domains, routing rules, stored
    messages, webhook delivery log.
    https://dashamail.ru/api/router/
    """

    # -- Domains ----------------------------------------------------------

    def domains(self):
        """GET /router/domains"""
        return self._client.request("GET", "/router/domains")

    def create_domain(self, domain):
        """POST /router/domains — connect your own inbound domain (needs an MX record)."""
        return self._client.request("POST", "/router/domains", None, {"domain": domain})

    def verify_domain(self, domain_id):
        """POST /router/domains/{domain_id}/verify — check the MX record."""
        return self._client.request("POST", "/router/domains/{}/verify".format(domain_id))

    def delete_domain(self, domain_id):
        """DELETE /router/domains/{domain_id}"""
        return self._client.request("DELETE", "/router/domains/{}".format(domain_id))

    def mx_instructions(self):
        """GET /router/domains/mx — DNS records to configure."""
        return self._client.request("GET", "/router/domains/mx")

    # -- Routes -------------------------------------------------------------

    def routes(self):
        """GET /router/routes"""
        return self._client.request("GET", "/router/routes")

    def get_route(self, route_id):
        """GET /router/routes/{route_id}"""
        return self._client.request("GET", "/router/routes/{}".format(route_id))

    def create_route(self, actions, **params):
        """POST /router/routes — actions is 1..5 action dicts, each with a "type" key (webhook, store, forward, stop)."""
        params["actions"] = actions
        return self._client.request("POST", "/router/routes", None, params)

    def update_route(self, route_id, **params):
        """PUT /router/routes/{route_id}"""
        return self._client.request("PUT", "/router/routes/{}".format(route_id), None, params)

    def delete_route(self, route_id):
        """DELETE /router/routes/{route_id}"""
        return self._client.request("DELETE", "/router/routes/{}".format(route_id))

    def rekey_route(self, route_id):
        """POST /router/routes/{route_id}/rekey — reissue the webhook signing key."""
        return self._client.request("POST", "/router/routes/{}/rekey".format(route_id))

    def reorder_routes(self, order):
        """POST /router/routes/reorder — order is a list of route ids in the desired priority order."""
        return self._client.request("POST", "/router/routes/reorder", None, {"order": order})

    # -- Stored messages ------------------------------------------------

    def messages(self, **params):
        """GET /router/messages"""
        return self._client.request("GET", "/router/messages", params)

    def get_message(self, message_id):
        """GET /router/messages/{message_id}"""
        return self._client.request("GET", "/router/messages/{}".format(message_id))

    def delete_message(self, message_id):
        """DELETE /router/messages/{message_id}"""
        return self._client.request("DELETE", "/router/messages/{}".format(message_id))

    def get_message_attachment(self, message_id, attachment_id):
        """GET /router/messages/{message_id}/attachments/{attachment_id}"""
        return self._client.request(
            "GET", "/router/messages/{}/attachments/{}".format(message_id, attachment_id)
        )

    # -- Webhook delivery log --------------------------------------------

    def deliveries(self, **params):
        """GET /router/deliveries"""
        return self._client.request("GET", "/router/deliveries", params)

    def get_delivery(self, delivery_id):
        """GET /router/deliveries/{delivery_id}"""
        return self._client.request("GET", "/router/deliveries/{}".format(delivery_id))

    # -- Settings -----------------------------------------------------------

    def settings(self):
        """GET /router/settings"""
        return self._client.request("GET", "/router/settings")

    def update_settings(self, **params):
        """PUT /router/settings — pass_autoreply, pass_list_mail"""
        return self._client.request("PUT", "/router/settings", None, params)
