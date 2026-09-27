from .base import BaseResource


class Templates(BaseResource):
    """
    Saved markup: legacy HTML-template store (/templates) plus saved campaigns
    in TEMPLATE status (/templates/saved), which is where the account UI keeps them.
    https://dashamail.ru/api/templates/
    """

    def all(self, **params):
        """GET /templates — legacy HTML templates."""
        return self._client.request("GET", "/templates", params)

    def get(self, id):
        """GET /templates/{id}"""
        return self._client.request("GET", "/templates/{}".format(id))

    def create(self, name, template, body, **params):
        """POST /templates — template is HTML markup, body is the plain-text markup."""
        params["name"] = name
        params["template"] = template
        params["body"] = body
        return self._client.request("POST", "/templates", None, params)

    def update(self, id, **params):
        """PUT /templates/{id}"""
        return self._client.request("PUT", "/templates/{}".format(id), None, params)

    def delete(self, id):
        """DELETE /templates/{id}"""
        return self._client.request("DELETE", "/templates/{}".format(id))

    def saved(self, **params):
        """GET /templates/saved — campaigns saved as reusable templates (status TEMPLATE)."""
        return self._client.request("GET", "/templates/saved", params)
