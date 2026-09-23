import base64
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from fake_client import FakeClient  # noqa: E402
from dashamail.resources.images import Images  # noqa: E402
from dashamail.resources.lists import Lists  # noqa: E402
from dashamail.resources.transactional import Transactional  # noqa: E402


def ok(data, meta=None):
    body = {"response": {"msg": {"err_code": 0, "text": "OK", "type": "message"}, "data": data}}
    if meta:
        body["meta"] = meta
    return body


class ResourceTest(unittest.TestCase):
    def test_lists_create_sends_name_in_body(self):
        client = FakeClient()
        client.queue_response(201, ok({"list_id": 42}))
        lists = Lists(client)

        result = lists.create("Клиенты", company="ООО Ромашка")

        self.assertEqual(result["list_id"], 42)
        call = client.calls[0]
        self.assertEqual(call["method"], "POST")
        self.assertTrue(call["url"].endswith("/lists"))
        decoded = json.loads(call["data"].decode("utf-8"))
        self.assertEqual(decoded["name"], "Клиенты")
        self.assertEqual(decoded["company"], "ООО Ромашка")

    def test_lists_get_member_encodes_email_in_path(self):
        client = FakeClient()
        client.queue_response(200, ok({"email": "a+b@example.com"}))
        lists = Lists(client)

        lists.get_member(1, "a+b@example.com")

        self.assertIn("a%2Bb%40example.com", client.calls[0]["url"])

    def test_lists_move_member_sends_required_fields(self):
        client = FakeClient()
        client.queue_response(200, ok(None))
        lists = Lists(client)

        lists.move_member(1, "a@example.com", 2, 555)

        decoded = json.loads(client.calls[0]["data"].decode("utf-8"))
        self.assertEqual(decoded["to_list_id"], 2)
        self.assertEqual(decoded["member_id"], 555)

    def test_lists_find_member_hits_account_wide_endpoint(self):
        client = FakeClient()
        client.queue_response(200, ok([{"list_id": 1, "email": "a@example.com"}]))
        lists = Lists(client)

        lists.find_member("a@example.com")

        self.assertIn("/members?", client.calls[0]["url"])
        self.assertIn("email=a%40example.com", client.calls[0]["url"])

    def test_transactional_send_builds_body(self):
        client = FakeClient()
        client.queue_response(201, ok({"transaction_id": "abc"}))
        transactional = Transactional(client)

        result = transactional.send("to@example.com", "from@yourdomain.com", "<p>Hi</p>", subject="Hello")

        self.assertEqual(result["transaction_id"], "abc")
        decoded = json.loads(client.calls[0]["data"].decode("utf-8"))
        self.assertEqual(decoded["to"], "to@example.com")
        self.assertEqual(decoded["from_email"], "from@yourdomain.com")
        self.assertEqual(decoded["message"], "<p>Hi</p>")
        self.assertEqual(decoded["subject"], "Hello")

    def test_images_optimize_base64_encodes_binary_data(self):
        client = FakeClient()
        client.queue_response(200, ok({"image": base64.b64encode(b"binary").decode(), "saved_bytes": 10}))
        images = Images(client)

        images.optimize(b"raw-bytes", max_width=800)

        decoded = json.loads(client.calls[0]["data"].decode("utf-8"))
        self.assertEqual(decoded["image"], base64.b64encode(b"raw-bytes").decode())
        self.assertEqual(decoded["max_width"], 800)

    def test_paginated_members_exposes_has_more(self):
        client = FakeClient()
        client.queue_response(200, ok([{"email": "a@example.com"}], meta={"has_more": True, "limit": 100}))
        lists = Lists(client)

        result = lists.members(1)

        self.assertTrue(result.has_more())
        self.assertEqual(result.get_limit(), 100)


if __name__ == "__main__":
    unittest.main()
