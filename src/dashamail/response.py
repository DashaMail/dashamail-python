"""Response wrapper returned by every successful DashaMail API call."""


class Response:
    """
    Wraps the ``data`` payload of a successful API call together with its
    ``meta`` (pagination info) and the human-readable ``msg.text`` DashaMail
    sent.

    Behaves like the underlying list/dict so most callers never need to know
    it exists::

        members = dashamail.lists.members(list_id)
        for member in members:
            print(member["email"])
        print(members[0]["email"])
        print(len(members))

    Paginated endpoints (``members()`` and friends) additionally expose
    ``has_more()``/``get_limit()`` taken from the ``meta`` object DashaMail
    returns instead of a total count.
    """

    def __init__(self, data, meta=None, message=None):
        self.data = data
        self.meta = meta or {}
        self.message = message

    def has_more(self):
        """True when a paginated listing has more rows beyond the returned page."""
        return bool(self.meta.get("has_more"))

    def get_limit(self):
        """The effective page size DashaMail used to answer a paginated listing."""
        limit = self.meta.get("limit")
        return int(limit) if limit is not None else None

    def __iter__(self):
        return iter(self.data) if self.data is not None else iter(())

    def __len__(self):
        return len(self.data) if self.data is not None else 0

    def __getitem__(self, key):
        return self.data[key]

    def __contains__(self, item):
        return item in self.data if self.data is not None else False

    def __eq__(self, other):
        if isinstance(other, Response):
            return self.data == other.data
        return self.data == other

    def __repr__(self):
        return "Response(data={!r}, meta={!r})".format(self.data, self.meta)
