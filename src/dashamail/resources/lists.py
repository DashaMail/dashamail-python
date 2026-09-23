from urllib.parse import quote

from .base import BaseResource


class Lists(BaseResource):
    """
    Address lists (address books), their subscribers and merge fields.
    https://dashamail.ru/api/lists/
    """

    def all(self, **params):
        """GET /lists — all address lists, newest first."""
        return self._client.request("GET", "/lists", params)

    def get(self, list_id, **params):
        """GET /lists/{list_id}"""
        return self._client.request("GET", "/lists/{}".format(list_id), params)

    def create(self, name, **params):
        """POST /lists"""
        params["name"] = name
        return self._client.request("POST", "/lists", None, params)

    def update(self, list_id, **params):
        """PUT /lists/{list_id}"""
        return self._client.request("PUT", "/lists/{}".format(list_id), None, params)

    def delete(self, list_id):
        """DELETE /lists/{list_id}"""
        return self._client.request("DELETE", "/lists/{}".format(list_id))

    # -- Members --------------------------------------------------------

    def members(self, list_id, **params):
        """GET /lists/{list_id}/members — start, limit, order, state, email, member_id, segment_id"""
        return self._client.request("GET", "/lists/{}/members".format(list_id), params)

    def get_member(self, list_id, email):
        """GET /lists/{list_id}/members/{email}"""
        return self._client.request("GET", "/lists/{}/members/{}".format(list_id, quote(email, safe="")))

    def add_member(self, list_id, email, **params):
        """POST /lists/{list_id}/members — merge_1..merge_N and the rest go in kwargs."""
        params["email"] = email
        return self._client.request("POST", "/lists/{}/members".format(list_id), None, params)

    def add_members_batch(self, list_id, batch, **params):
        """POST /lists/{list_id}/members/batch — batch is a list of member dicts, each at least {"email": ...}."""
        params["batch"] = batch
        return self._client.request("POST", "/lists/{}/members/batch".format(list_id), None, params)

    def import_members(self, list_id, email, type, **params):
        """POST /lists/{list_id}/members/import — import subscribers from a file."""
        params["email"] = email
        params["type"] = type
        return self._client.request("POST", "/lists/{}/members/import".format(list_id), None, params)

    def get_import_result(self, list_id):
        """GET /lists/{list_id}/members/import — result of the last import job."""
        return self._client.request("GET", "/lists/{}/members/import".format(list_id))

    def get_import_history(self, list_id, **params):
        """GET /lists/{list_id}/import-history"""
        return self._client.request("GET", "/lists/{}/import-history".format(list_id), params)

    def update_member(self, list_id, email, **params):
        """PUT /lists/{list_id}/members/{email}"""
        return self._client.request("PUT", "/lists/{}/members/{}".format(list_id, quote(email, safe="")), None, params)

    def delete_member(self, list_id, email, member_id):
        """DELETE /lists/{list_id}/members/{email}"""
        return self._client.request(
            "DELETE", "/lists/{}/members/{}".format(list_id, quote(email, safe="")), None, {"member_id": member_id}
        )

    def find_member(self, email):
        """GET /members — find a subscriber address across every list in the account."""
        return self._client.request("GET", "/members", {"email": email})

    def unsubscribe_member(self, list_id, email, **params):
        """POST /lists/{list_id}/members/{email}/unsubscribe"""
        return self._client.request(
            "POST", "/lists/{}/members/{}/unsubscribe".format(list_id, quote(email, safe="")), None, params
        )

    def move_member(self, list_id, email, to_list_id, member_id):
        """POST /lists/{list_id}/members/{email}/move — move a subscriber to another list."""
        return self._client.request(
            "POST",
            "/lists/{}/members/{}/move".format(list_id, quote(email, safe="")),
            None,
            {"to_list_id": to_list_id, "member_id": member_id},
        )

    def copy_member(self, list_id, email, to_list_id, member_id):
        """POST /lists/{list_id}/members/{email}/copy — copy a subscriber to another list."""
        return self._client.request(
            "POST",
            "/lists/{}/members/{}/copy".format(list_id, quote(email, safe="")),
            None,
            {"to_list_id": to_list_id, "member_id": member_id},
        )

    def member_activity(self, list_id, email, **params):
        """GET /lists/{list_id}/members/{email}/activity"""
        return self._client.request(
            "GET", "/lists/{}/members/{}/activity".format(list_id, quote(email, safe="")), params
        )

    def last_status(self, list_id, email):
        """GET /lists/{list_id}/last-status — current subscription state of an address."""
        return self._client.request("GET", "/lists/{}/last-status".format(list_id), {"email": email})

    def check_email(self, list_id, email):
        """GET /lists/{list_id}/check-email — validate an address before subscribing it."""
        return self._client.request("GET", "/lists/{}/check-email".format(list_id), {"email": email})

    def clean(self, list_id, **params):
        """POST /lists/{list_id}/clean — purge bounced/complained/unsubscribed members."""
        return self._client.request("POST", "/lists/{}/clean".format(list_id), None, params)

    def unsubscribed(self, list_id, **params):
        """GET /lists/{list_id}/unsubscribed"""
        return self._client.request("GET", "/lists/{}/unsubscribed".format(list_id), params)

    def complaints(self, list_id, **params):
        """GET /lists/{list_id}/complaints"""
        return self._client.request("GET", "/lists/{}/complaints".format(list_id), params)

    # -- Merge fields -----------------------------------------------------

    def add_field(self, list_id, type, **params):
        """POST /lists/{list_id}/fields — type is one of the merge field types, e.g. "text", "choice"."""
        params["type"] = type
        return self._client.request("POST", "/lists/{}/fields".format(list_id), None, params)

    def update_field(self, list_id, merge_id, **params):
        """PUT /lists/{list_id}/fields/{merge_id}"""
        params["merge_id"] = merge_id
        return self._client.request("PUT", "/lists/{}/fields/{}".format(list_id, merge_id), None, params)

    def delete_field(self, list_id, merge_id):
        """DELETE /lists/{list_id}/fields/{merge_id}"""
        return self._client.request("DELETE", "/lists/{}/fields/{}".format(list_id, merge_id))
