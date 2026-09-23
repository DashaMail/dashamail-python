import os

from dashamail import DashaMail, ApiException, RateLimitException

dashamail = DashaMail(os.environ.get("DASHAMAIL_API_KEY", "YOUR_API_KEY"))

try:
    # Account balance.
    balance = dashamail.account.balance()
    print("Balance: {} {}".format(balance["balance"], balance["currency"]))

    # Create a list and add a subscriber.
    created = dashamail.lists.create("Example list")
    list_id = created["list_id"]

    dashamail.lists.add_member(list_id, "subscriber@example.com", merge_1="Иван")

    # Iterate subscribers, page by page.
    start = 0
    while True:
        page = dashamail.lists.members(list_id, start=start, limit=100)
        for member in page:
            print(member["email"])
        start += page.get_limit()
        if not page.has_more():
            break

    # Send a transactional email.
    dashamail.transactional.send(
        "subscriber@example.com",
        "sender@yourdomain.com",
        "<p>Спасибо за подписку!</p>",
        subject="Добро пожаловать",
    )
except RateLimitException as e:
    print("Rate limited, retry after {}s".format(e.get_retry_after()))
except ApiException as e:
    print("DashaMail API error {}: {}".format(e.api_code, e))
