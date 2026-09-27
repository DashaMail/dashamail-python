import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from fake_client import FakeClient  # noqa: E402
from dashamail.exceptions import (  # noqa: E402
    AuthenticationException,
    NotFoundException,
    RateLimitException,
    ValidationException,
)
from dashamail.response import Response  # noqa: E402


def ok(data, meta=None, message="OK"):
    body = {"response": {"msg": {"err_code": 0, "text": message, "type": "message"}, "data": data}}
    if meta:
        body["meta"] = meta
    return body


class ClientTest(unittest.TestCase):
    def test_successful_request_unwraps_response_data(self):
        client = FakeClient()
        client.queue_response(200, ok([{"id": 1, "name": "Клиенты"}]))

        result = client.request("GET", "/lists")

        self.assertIsInstance(result, Response)
        self.assertEqual(result.data, [{"id": 1, "name": "Клиенты"}])
        self.assertEqual(result.message, "OK")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["id"], 1)

    def test_pagination_meta_is_exposed(self):
        client = FakeClient()
        client.queue_response(200, ok([1, 2, 3], meta={"has_more": True, "limit": 3}))

        result = client.request("GET", "/lists/1/members")

        self.assertTrue(result.has_more())
        self.assertEqual(result.get_limit(), 3)

    def test_204_no_content_returns_none(self):
        client = FakeClient()
        client.queue_response(204, b"")

        result = client.request("DELETE", "/lists/1")

        self.assertIsNone(result)

    def test_authorization_header_is_sent(self):
        client = FakeClient(api_key="secret-key-123")
        client.queue_response(200, ok([]))

        client.request("GET", "/lists")

        self.assertEqual(client.calls[0]["headers"]["Authorization"], "Bearer secret-key-123")

    def test_json_body_is_encoded_and_content_type_set(self):
        client = FakeClient()
        client.queue_response(201, ok({"list_id": 5}))

        client.request("POST", "/lists", None, {"name": "Тест"})

        self.assertEqual(client.calls[0]["headers"]["Content-Type"], "application/json")
        self.assertEqual(json.loads(client.calls[0]["data"].decode("utf-8")), {"name": "Тест"})

    def test_error_statuses_map_to_exception_classes(self):
        cases = [
            (401, AuthenticationException),
            (404, NotFoundException),
            (422, ValidationException),
            (429, RateLimitException),
        ]
        for status, expected_cls in cases:
            with self.subTest(status=status):
                client = FakeClient()
                client.queue_response(status, {"error": {"code": 999, "message": "boom", "details": {}}})
                with self.assertRaises(expected_cls):
                    client.request("GET", "/whatever")

    def test_rate_limit_exposes_retry_after_from_details(self):
        client = FakeClient()
        client.queue_response(
            429,
            {"error": {"code": 58, "message": "Limit", "details": {"limit_per_minute": 120, "retry_after": 60}}},
        )

        with self.assertRaises(RateLimitException) as ctx:
            client.request("GET", "/lists")

        self.assertEqual(ctx.exception.get_retry_after(), 60)
        self.assertEqual(ctx.exception.api_code, 58)

    def test_query_params_are_appended_to_url(self):
        client = FakeClient()
        client.queue_response(200, ok([]))

        client.request("GET", "/lists", {"state": "active"})

        self.assertIn("state=active", client.calls[0]["url"])


if __name__ == "__main__":
    unittest.main()
