from .base import BaseResource


class Reports(BaseResource):
    """
    Campaign statistics: sent/delivered/opened/clicked/bounced, click and bounce
    breakdowns, geography, mail clients, event feed, A/B test results.
    https://dashamail.ru/api/reports/
    """

    def summary(self, campaign_id, **params):
        """GET /reports/{campaign_id}/summary"""
        return self._client.request("GET", "/reports/{}/summary".format(campaign_id), params)

    def timeline(self, campaign_id, **params):
        """GET /reports/{campaign_id}/timeline — metric values bucketed over time."""
        return self._client.request("GET", "/reports/{}/timeline".format(campaign_id), params)

    def ab(self, campaign_id):
        """GET /reports/{campaign_id}/variants — A/B test results."""
        return self._client.request("GET", "/reports/{}/variants".format(campaign_id))

    def compare(self, periods, **params):
        """POST /reports/compare — compare metrics across periods/campaigns/lists."""
        params["periods"] = periods
        return self._client.request("POST", "/reports/compare", None, params)

    def metric(self, campaign_id, metric, **params):
        """GET /reports/{campaign_id}/{metric} — recipient list for one event."""
        return self._client.request("GET", "/reports/{}/{}".format(campaign_id, metric), params)

    def sent(self, campaign_id, **params):
        """GET /reports/{campaign_id}/sent"""
        return self.metric(campaign_id, "sent", **params)

    def delivered(self, campaign_id, **params):
        """GET /reports/{campaign_id}/delivered"""
        return self.metric(campaign_id, "delivered", **params)

    def opened(self, campaign_id, **params):
        """GET /reports/{campaign_id}/opened"""
        return self.metric(campaign_id, "opened", **params)

    def clicked(self, campaign_id, **params):
        """GET /reports/{campaign_id}/clicked"""
        return self.metric(campaign_id, "clicked", **params)

    def bounced(self, campaign_id, **params):
        """GET /reports/{campaign_id}/bounced"""
        return self.metric(campaign_id, "bounced", **params)

    def complained(self, campaign_id, **params):
        """GET /reports/{campaign_id}/complained"""
        return self.metric(campaign_id, "complained", **params)

    def unsubscribed(self, campaign_id, **params):
        """GET /reports/{campaign_id}/unsubscribed"""
        return self.metric(campaign_id, "unsubscribed", **params)

    def events(self, campaign_id, **params):
        """GET /reports/{campaign_id}/events — full event feed with filters."""
        return self._client.request("GET", "/reports/{}/events".format(campaign_id), params)

    def clickstat(self, campaign_id):
        """GET /reports/{campaign_id}/clickstat — clicks broken down by link."""
        return self._client.request("GET", "/reports/{}/clickstat".format(campaign_id))

    def userclicks(self, campaign_id, url):
        """GET /reports/{campaign_id}/userclicks — who clicked a specific link."""
        return self._client.request("GET", "/reports/{}/userclicks".format(campaign_id), {"url": url})

    def bouncestat(self, campaign_id):
        """GET /reports/{campaign_id}/bouncestat — bounces broken down by SMTP code."""
        return self._client.request("GET", "/reports/{}/bouncestat".format(campaign_id))

    def domains(self, campaign_id, **params):
        """GET /reports/{campaign_id}/domains — metrics broken down by recipient mail domain."""
        return self._client.request("GET", "/reports/{}/domains".format(campaign_id), params)

    def geo(self, campaign_id):
        """GET /reports/{campaign_id}/geo — geography of opens."""
        return self._client.request("GET", "/reports/{}/geo".format(campaign_id))

    def clients(self, campaign_id):
        """GET /reports/{campaign_id}/clients — mail clients and devices."""
        return self._client.request("GET", "/reports/{}/clients".format(campaign_id))

    def codes(self, campaign_id, **params):
        """GET /reports/{campaign_id}/codes — confirmation codes."""
        return self._client.request("GET", "/reports/{}/codes".format(campaign_id), params)
