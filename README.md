# dashamail-python

Official Python SDK for the [DashaMail REST API v2](https://dashamail.ru/api/) — address
lists, campaigns, automations, transactional email, reports, dialogs, inbound mail routing
and image optimization, from a single client with no third-party dependencies.

## Requirements

- Python 3.7 or newer (standard library only — `urllib`, `json`)

## Installation

```bash
pip install dashamail-python
```

The distribution is named `dashamail-python` (the bare `dashamail` name on PyPI belongs to an
unrelated third-party project), but the import stays `import dashamail`.

## Getting an API key

Личный кабинет → Аккаунт → API и интеграции. Treat it like a password: it acts on behalf
of the whole account.

## Quickstart

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

See [`examples/quickstart.py`](examples/quickstart.py) for a fuller walkthrough, and
[dashamail.ru/api](https://dashamail.ru/api/) for the full parameter reference of every
endpoint — the SDK mirrors it method-for-method. Optional parameters are passed as keyword
arguments matching the API's field names.

## Resources

`DashaMail` exposes one attribute per section of the API. Every method returns a
[`dashamail.Response`](src/dashamail/response.py) (behaves like the underlying list/dict)
or raises a `dashamail.ApiException`.

| Attribute         | Class                          | Covers |
|-------------------|----------------------------------|--------|
| `.lists`          | `dashamail.resources.Lists`         | Address lists, subscribers, merge fields, imports |
| `.segments`       | `dashamail.resources.Segments`      | Saved subscriber segments |
| `.campaigns`      | `dashamail.resources.Campaigns`     | Bulk campaigns: draft, launch, pause, A/B tests, attachments, folders |
| `.automations`    | `dashamail.resources.Automations`   | Event-triggered emails |
| `.workflows`      | `dashamail.resources.Workflows`     | Visual-builder automation scenarios |
| `.templates`      | `dashamail.resources.Templates`     | Saved HTML templates and templated campaigns |
| `.reports`        | `dashamail.resources.Reports`       | Campaign statistics, events, click/bounce/geo breakdowns, A/B results |
| `.transactional`  | `dashamail.resources.Transactional` | One-off transactional email: send, status, log, stats |
| `.account`        | `dashamail.resources.Account`       | Balance, senders, sending domains, webhooks |
| `.dialogs`        | `dashamail.resources.Dialogs`       | Subscriber replies to campaigns |
| `.router`         | `dashamail.resources.Router`        | Inbound mail: domains, routing rules, stored messages |
| `.images`         | `dashamail.resources.Images`        | Resize/recompress an image before using it in a campaign |

## Working with responses

```python
members = dashamail.lists.members(list_id, limit=100)

for member in members:          # Response is iterable
    print(member["email"])

len(members)                    # number of rows in this page
members.data                    # the raw list/dict, if you'd rather not iterate
members.has_more()              # true if there's another page (see Pagination below)
```

## Pagination

List endpoints (`lists.members()`, `lists.unsubscribed()`, `transactional.log()`, ...)
don't return a total count — DashaMail tells you instead whether there's another page:

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

## Error handling

Every non-2xx response raises a subclass of `dashamail.ApiException`, chosen by HTTP status:

| Exception                  | HTTP status |
|-----------------------------|------|
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
    # e.api_code     — DashaMail's own stable error code (see https://dashamail.ru/api/errors/)
    # e.http_status  — the HTTP status of the response
    # e.details      — any extra structured context the API attached
    logging.error("%s: %s", e.api_code, e)
```

A request that never got an HTTP response at all (DNS, TLS, timeout...) raises
`dashamail.NetworkException` instead.

## Images

`POST /images/optimize` is the one endpoint that isn't plain JSON in and out:

```python
# From bytes already in memory:
with open("banner.png", "rb") as f:
    result = dashamail.images.optimize(f.read(), max_width=1600)
with open("banner-optimized.png", "wb") as f:
    f.write(base64.b64decode(result["image"]))

# Straight from disk, without loading it into a Python bytes object first:
result = dashamail.images.optimize_file("/path/to/banner.png")

# Same, but skip the base64 round-trip and get raw bytes back:
binary = dashamail.images.optimize_file_binary("/path/to/banner.png")
binary.save_to("/path/to/banner-optimized.png")
```

## Advanced configuration

```python
dashamail = DashaMail(
    "YOUR_API_KEY",
    timeout=60,                                # seconds, default 30
    base_url="https://api.dashamail.com/v2",   # override for testing/proxying
    user_agent="my-app/1.0 (+dashamail-python)",
)

# Escape hatch for an endpoint the SDK doesn't wrap yet:
dashamail.client.request("GET", "/some/new/endpoint", {"foo": "bar"})
```

## Testing

```bash
pip install -e .
python -m unittest discover -s tests -v
```

## License

MIT, see [LICENSE](LICENSE).
