from .base import BaseResource


class Campaigns(BaseResource):
    """
    Bulk campaigns: draft, build, launch, pause, A/B tests, attachments, folders.
    https://dashamail.ru/api/campaigns/
    """

    def all(self, **params):
        """GET /campaigns"""
        return self._client.request("GET", "/campaigns", params)

    def get(self, campaign_id, **params):
        """GET /campaigns/{campaign_id}"""
        return self._client.request("GET", "/campaigns/{}".format(campaign_id), params)

    def create(self, **params):
        """POST /campaigns — requires list_id, subject, from_email, from_name; see the API docs for the rest."""
        return self._client.request("POST", "/campaigns", None, params)

    def update(self, campaign_id, **params):
        """PUT /campaigns/{campaign_id}"""
        return self._client.request("PUT", "/campaigns/{}".format(campaign_id), None, params)

    def delete(self, campaign_id):
        """DELETE /campaigns/{campaign_id}"""
        return self._client.request("DELETE", "/campaigns/{}".format(campaign_id))

    def copy(self, campaign_id, **params):
        """POST /campaigns/{campaign_id}/copy"""
        return self._client.request("POST", "/campaigns/{}/copy".format(campaign_id), None, params)

    def pause(self, campaign_id):
        """POST /campaigns/{campaign_id}/pause"""
        return self._client.request("POST", "/campaigns/{}/pause".format(campaign_id))

    def resume(self, campaign_id):
        """POST /campaigns/{campaign_id}/resume"""
        return self._client.request("POST", "/campaigns/{}/resume".format(campaign_id))

    def schedule(self, campaign_id, delivery_time, **params):
        """POST /campaigns/{campaign_id}/schedule"""
        params["delivery_time"] = delivery_time
        return self._client.request("POST", "/campaigns/{}/schedule".format(campaign_id), None, params)

    def send(self, campaign_id):
        """POST /campaigns/{campaign_id}/send — send a draft right now."""
        return self._client.request("POST", "/campaigns/{}/send".format(campaign_id))

    def unschedule(self, campaign_id):
        """POST /campaigns/{campaign_id}/unschedule — pull a scheduled campaign back to DRAFT."""
        return self._client.request("POST", "/campaigns/{}/unschedule".format(campaign_id))

    def test(self, campaign_id, email):
        """POST /campaigns/{campaign_id}/test — send a test copy to your own address."""
        return self._client.request("POST", "/campaigns/{}/test".format(campaign_id), None, {"email": email})

    def preview(self, campaign_id):
        """GET /campaigns/{campaign_id}/preview — browser preview link."""
        return self._client.request("GET", "/campaigns/{}/preview".format(campaign_id))

    def estimate(self, campaign_id):
        """GET /campaigns/{campaign_id}/estimate — how many emails would be sent."""
        return self._client.request("GET", "/campaigns/{}/estimate".format(campaign_id))

    def resend(self, campaign_id, **params):
        """POST /campaigns/{campaign_id}/resend — resend to recipients who did not open."""
        return self._client.request("POST", "/campaigns/{}/resend".format(campaign_id), None, params)

    def get_attachments(self, campaign_id):
        """GET /campaigns/{campaign_id}/attachments"""
        return self._client.request("GET", "/campaigns/{}/attachments".format(campaign_id))

    def add_attachment(self, campaign_id, url, **params):
        """POST /campaigns/{campaign_id}/attachments — attach a file by URL."""
        params["url"] = url
        return self._client.request("POST", "/campaigns/{}/attachments".format(campaign_id), None, params)

    def delete_attachment(self, campaign_id, attachment_id):
        """DELETE /campaigns/{campaign_id}/attachments/{id}"""
        return self._client.request("DELETE", "/campaigns/{}/attachments/{}".format(campaign_id, attachment_id))

    def get_folders(self, **params):
        """GET /campaigns/folders"""
        return self._client.request("GET", "/campaigns/folders", params)

    def move_to_folder(self, campaign_id, folder_id):
        """POST /campaigns/{campaign_id}/move — move a campaign into a folder."""
        return self._client.request("POST", "/campaigns/{}/move".format(campaign_id), None, {"folder_id": folder_id})

    # -- A/B testing ------------------------------------------------------

    def create_ab(self, campaign_id, **params):
        """POST /campaigns/{campaign_id}/ab — turn a draft into an A/B test."""
        return self._client.request("POST", "/campaigns/{}/ab".format(campaign_id), None, params)

    def get_ab(self, campaign_id):
        """GET /campaigns/{campaign_id}/ab"""
        return self._client.request("GET", "/campaigns/{}/ab".format(campaign_id))

    def update_ab(self, campaign_id, **params):
        """PUT /campaigns/{campaign_id}/ab"""
        return self._client.request("PUT", "/campaigns/{}/ab".format(campaign_id), None, params)

    def delete_ab(self, campaign_id):
        """DELETE /campaigns/{campaign_id}/ab — dismantle the A/B test back into a plain campaign."""
        return self._client.request("DELETE", "/campaigns/{}/ab".format(campaign_id))

    def ab_winner(self, campaign_id, variant_id, delivery_time):
        """POST /campaigns/{campaign_id}/ab/winner — pick the winning variant and schedule the rest."""
        return self._client.request(
            "POST",
            "/campaigns/{}/ab/winner".format(campaign_id),
            None,
            {"variant_id": variant_id, "delivery_time": delivery_time},
        )

    def cancel_ab_winner(self, campaign_id):
        """DELETE /campaigns/{campaign_id}/ab/winner — cancel a previously chosen winner."""
        return self._client.request("DELETE", "/campaigns/{}/ab/winner".format(campaign_id))
