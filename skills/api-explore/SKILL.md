# Explore an API

Investigate a free/public API endpoint, understand its structure, and optionally generate a Python client.

## Steps

1. Hit the endpoint with a GET request (or the method the user specifies).
   - Use `curl` or `httpx` via Python.
   - Include any API key from `.env` if the user mentions one.
   - Respect rate limits — never spam an endpoint.
2. Inspect the response:
   - HTTP status code and content-type
   - Rate limit headers (X-RateLimit-*, Retry-After)
   - Pagination mechanism (offset, cursor, next URL)
   - Response body structure: keys, types, nesting depth
3. Show a sample response (truncated to first 3 items if it's a list).
4. Document the API: base URL, auth method, rate limits, response schema.
5. If the user asks, generate a minimal Python client with `httpx`.

## Examples

### API client generation

**BAD** — hardcoded keys, no error handling, no types:
```python
import requests
data = requests.get("https://api.example.com/data?key=abc123").json()
```

**GOOD** — env vars, typed response, retry on rate limit:
```python
import os
import httpx
from pydantic import BaseModel

class Item(BaseModel):
    id: int
    name: str
    value: float

API_KEY = os.environ["EXAMPLE_API_KEY"]
BASE_URL = "https://api.example.com"

async def get_items() -> list[Item]:
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{BASE_URL}/data",
            headers={"Authorization": f"Bearer {API_KEY}"},
            timeout=30.0,
        )
        resp.raise_for_status()
        return [Item(**item) for item in resp.json()["items"]]
```

### Pagination handling

**BAD** — only fetches first page:
```python
data = client.get("/items").json()
```

**GOOD** — follows pagination to completion:
```python
items = []
url = f"{BASE_URL}/items"
while url:
    resp = await client.get(url)
    data = resp.json()
    items.extend(data["results"])
    url = data.get("next")  # None when no more pages
```

## Notes

- Never hardcode API keys — always read from `.env` or environment variables
- Check PyPI for an existing SDK before writing a custom client
- If the API requires signup, tell the user and provide the signup URL
- For rate-limited APIs, add `asyncio.sleep()` between requests
