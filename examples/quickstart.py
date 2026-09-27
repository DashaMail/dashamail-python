import os

from dashamail import DashaMail, ApiException, RateLimitException

dashamail = DashaMail(os.environ.get("DASHAMAIL_API_KEY", "YOUR_API_KEY"))

try:
    # Баланс аккаунта.
    balance = dashamail.account.balance()
    print("Баланс: {} {}".format(balance["balance"], balance["currency"]))

    # Создаём базу и добавляем подписчика.
    created = dashamail.lists.create("Example list")
    list_id = created["list_id"]

    dashamail.lists.add_member(list_id, "subscriber@example.com", merge_1="Иван")

    # Перебираем подписчиков постранично.
    start = 0
    while True:
        page = dashamail.lists.members(list_id, start=start, limit=100)
        for member in page:
            print(member["email"])
        start += page.get_limit()
        if not page.has_more():
            break

    # Отправляем транзакционное письмо.
    dashamail.transactional.send(
        "subscriber@example.com",
        "sender@yourdomain.com",
        "<p>Спасибо за подписку!</p>",
        subject="Добро пожаловать",
    )
except RateLimitException as e:
    print("Превышен лимит запросов, повтор через {} с".format(e.get_retry_after()))
except ApiException as e:
    print("Ошибка DashaMail API {}: {}".format(e.api_code, e))
