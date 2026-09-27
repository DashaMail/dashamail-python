# dashamail-python

Официальный Python SDK для [DashaMail REST API v2](https://dashamail.ru/api/) — адресные
базы, рассылки, автоматизации, транзакционные письма, отчёты, диалоги, обработка входящей
почты и оптимизация изображений из одного клиента без сторонних зависимостей.

## Требования

- Python 3.7 или новее (только стандартная библиотека — `urllib`, `json`)

## Установка

```bash
pip install dashamail-python
```

Дистрибутив называется `dashamail-python` (голое имя `dashamail` на PyPI занято сторонним
неофициальным проектом), но импорт остаётся прежним — `import dashamail`.

## Где взять API-ключ

Личный кабинет → Аккаунт → API и интеграции. Обращайтесь с ним как с паролем: он действует
от имени всего аккаунта.

## Быстрый старт

```python
from dashamail import DashaMail

dashamail = DashaMail("YOUR_API_KEY")

balance = dashamail.account.balance()
print(balance["balance"])

created = dashamail.lists.create("Newsletter")
dashamail.lists.add_member(created["list_id"], "subscriber@example.com", merge_1="Иван")

dashamail.transactional.send(
    "subscriber@example.com",
    "sender@yourdomain.com",
    "<p>Спасибо за подписку!</p>",
    subject="Добро пожаловать",
)
```

Более полный пример — в [`examples/quickstart.py`](examples/quickstart.py), а полный
справочник параметров каждого эндпоинта — на [dashamail.ru/api](https://dashamail.ru/api/):
SDK повторяет его метод в метод. Необязательные параметры передаются именованными
аргументами с теми же именами полей, что и в API.

## Ресурсы

`DashaMail` — это объект с одним атрибутом на каждый раздел API. Каждый метод возвращает
[`dashamail.Response`](src/dashamail/response.py) (ведёт себя как обёрнутый список/словарь)
либо поднимает `dashamail.ApiException`.

| Атрибут            | Класс                                | Что покрывает |
|--------------------|----------------------------------------|--------|
| `.lists`           | `dashamail.resources.Lists`         | Адресные базы, подписчики, дополнительные поля, импорт |
| `.segments`        | `dashamail.resources.Segments`      | Сохранённые сегменты подписчиков |
| `.campaigns`       | `dashamail.resources.Campaigns`     | Рассылки: черновик, запуск, пауза, A/B-тесты, вложения, папки |
| `.automations`     | `dashamail.resources.Automations`   | Письма по событиям подписчика |
| `.workflows`       | `dashamail.resources.Workflows`     | Сценарии визуального конструктора |
| `.templates`       | `dashamail.resources.Templates`     | Сохранённые HTML-шаблоны и шаблонные рассылки |
| `.reports`         | `dashamail.resources.Reports`       | Статистика рассылок, лента событий, разбивки по кликам/возвратам/гео, результаты A/B |
| `.transactional`   | `dashamail.resources.Transactional` | Одиночные транзакционные письма: отправка, статус, журнал, статистика |
| `.account`         | `dashamail.resources.Account`       | Баланс, отправители, домены отправки, webhooks |
| `.dialogs`         | `dashamail.resources.Dialogs`       | Ответы подписчиков на рассылки |
| `.router`          | `dashamail.resources.Router`        | Обработка входящей почты: домены, правила маршрутизации, сохранённые письма |
| `.images`          | `dashamail.resources.Images`        | Уменьшение веса изображения перед вставкой в рассылку |

## Работа с ответом

```python
members = dashamail.lists.members(list_id, limit=100)

for member in members:          # Response — итерируемый объект
    print(member["email"])

len(members)                    # число записей на этой странице
members.data                    # сырой список/словарь, если перебирать не нужно
members.has_more()              # true, если есть следующая страница (см. «Пагинация» ниже)
```

## Пагинация

Списочные эндпоинты (`lists.members()`, `lists.unsubscribed()`, `transactional.log()` и
другие) не возвращают общее количество записей — вместо этого DashaMail сообщает, есть ли
ещё страница:

```python
start = 0
while True:
    page = dashamail.lists.members(list_id, start=start, limit=100)
    for member in page:
        ...
    start += page.get_limit()
    if not page.has_more():
        break
```

## Обработка ошибок

Любой ответ не из диапазона 2xx поднимает подкласс `dashamail.ApiException`, выбранный по
HTTP-статусу:

| Исключение                  | HTTP-статус |
|------------------------------|------|
| `AuthenticationException`   | 401 |
| `PaymentRequiredException`  | 402 |
| `AuthorizationException`    | 403 |
| `NotFoundException`         | 404 |
| `ConflictException`         | 409 |
| `PayloadTooLargeException`  | 413 |
| `ValidationException`       | 422 |
| `RateLimitException`        | 429 |
| `ServerException`           | 5xx |

```python
from dashamail import ApiException, RateLimitException

try:
    dashamail.campaigns.create(list_id=1, subject="Hi", from_email="a@b.com", from_name="A")
except RateLimitException as e:
    time.sleep(e.get_retry_after() or 60)
except ApiException as e:
    # e.api_code     — собственный устойчивый код ошибки DashaMail (см. https://dashamail.ru/api/errors/)
    # e.http_status  — HTTP-статус ответа
    # e.details      — дополнительный структурированный контекст от API, если есть
    logging.error("%s: %s", e.api_code, e)
```

Если ответ вообще не пришёл (обрыв DNS, TLS, таймаут...), поднимается
`dashamail.NetworkException`.

## Изображения

`POST /images/optimize` — единственный эндпоинт, у которого вход и выход не просто JSON:

```python
# Из байтов, уже загруженных в память:
with open("banner.png", "rb") as f:
    result = dashamail.images.optimize(f.read(), max_width=1600)
with open("banner-optimized.png", "wb") as f:
    f.write(base64.b64decode(result["image"]))

# Прямо с диска, без предварительной загрузки в объект bytes:
result = dashamail.images.optimize_file("/path/to/banner.png")

# То же самое, но без промежуточного base64 — сразу сырые байты:
binary = dashamail.images.optimize_file_binary("/path/to/banner.png")
binary.save_to("/path/to/banner-optimized.png")
```

## Расширенная настройка

```python
dashamail = DashaMail(
    "YOUR_API_KEY",
    timeout=60,                                # секунды, по умолчанию 30
    base_url="https://api.dashamail.com/v2",   # переопределить для тестов/прокси
    user_agent="my-app/1.0 (+dashamail-python)",
)

# Способ вызвать эндпоинт, для которого в SDK ещё нет отдельного метода:
dashamail.client.request("GET", "/some/new/endpoint", {"foo": "bar"})
```

## Тесты

```bash
pip install -e .
python -m unittest discover -s tests -v
```

## Лицензия

MIT, см. [LICENSE](LICENSE).
