from .client import Client
from .resources import (
    Account,
    Automations,
    Campaigns,
    Dialogs,
    Images,
    Lists,
    Reports,
    Router,
    Segments,
    Templates,
    Transactional,
    Workflows,
)


class DashaMail:
    """
    Entry point of the DashaMail Python SDK.

        dashamail = DashaMail("YOUR_API_KEY")
        lists = dashamail.lists.all()
        dashamail.transactional.send("user@example.com", "sender@yourdomain.com", "<p>Hi!</p>")
    """

    def __init__(self, api_key, base_url=None, timeout=30, user_agent=None):
        """
        :param api_key: Account API key — Личный кабинет → Аккаунт → API и интеграции.
        :param base_url: Override the API origin, e.g. for a proxy or a mock server.
        :param timeout: Request timeout in seconds. Default 30.
        :param user_agent: Override the User-Agent header.
        """
        self.client = Client(api_key, base_url=base_url, timeout=timeout, user_agent=user_agent)

        self.lists = Lists(self.client)
        self.segments = Segments(self.client)
        self.campaigns = Campaigns(self.client)
        self.automations = Automations(self.client)
        self.workflows = Workflows(self.client)
        self.templates = Templates(self.client)
        self.reports = Reports(self.client)
        self.transactional = Transactional(self.client)
        self.account = Account(self.client)
        self.dialogs = Dialogs(self.client)
        self.router = Router(self.client)
        self.images = Images(self.client)
