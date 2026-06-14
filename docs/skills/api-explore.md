# API Explore

Investigate a public or authenticated API endpoint, understand its response structure, and optionally generate a typed Python client with proper error handling, pagination, and rate-limit awareness.

## How It Works

1. **Hit the endpoint** -- Send a request using `curl` or `httpx`. Include any API key from `.env` if specified.
2. **Inspect the response** -- Examine the HTTP status code, content type, rate-limit headers (`X-RateLimit-*`, `Retry-After`), and pagination mechanism (offset, cursor, next URL).
3. **Show a sample** -- Display the response body, truncated to the first 3 items if it is a list.
4. **Document the API** -- Summarize the base URL, authentication method, rate limits, and response schema.
5. **Generate a client** -- If requested, produce a minimal async Python client using `httpx` with Pydantic response models.

## Example: Exploring a Public API

```bash
$ curl -s "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd" | python -m json.tool
{
    "bitcoin": {
        "usd": 67432.0
    }
}
```

After inspecting the response, a typed client can be generated:

```python
import httpx
from pydantic import BaseModel


class PriceResponse(BaseModel):
    usd: float
    usd_24h_change: float | None = None


async def get_price(coin_id: str) -> PriceResponse:
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            "https://api.coingecko.com/api/v3/simple/price",
            params={
                "ids": coin_id,
                "vs_currencies": "usd",
                "include_24hr_change": "true",
            },
            timeout=30.0,
        )
        resp.raise_for_status()
        data = resp.json()[coin_id]
        return PriceResponse(**data)
```

## API Client Patterns

!!! warning "Bad: hardcoded keys, no error handling, no types"
    ```python
    import requests
    data = requests.get("https://api.example.com/data?key=abc123").json()
    ```

!!! example "Good: env vars, typed response, retry on rate limit"
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

## Pagination Handling

!!! warning "Bad: only fetches the first page"
    ```python
    data = client.get("/items").json()
    ```

!!! example "Good: follows pagination to completion"
    ```python
    items: list[Item] = []
    url = f"{BASE_URL}/items"
    while url:
        resp = await client.get(url)
        resp.raise_for_status()
        data = resp.json()
        items.extend(Item(**r) for r in data["results"])
        url = data.get("next")  # None when exhausted
    ```

## Rate Limit Handling

When an API returns `429 Too Many Requests`, the client should respect the `Retry-After` header:

```python
import asyncio

async def get_with_retry(client: httpx.AsyncClient, url: str) -> dict:
    for attempt in range(3):
        resp = await client.get(url)
        if resp.status_code == 429:
            wait = int(resp.headers.get("Retry-After", 5))
            await asyncio.sleep(wait)
            continue
        resp.raise_for_status()
        return resp.json()
    raise RuntimeError("Rate limit exceeded after 3 retries")
```

## Notes

- Never hardcode API keys. Always read from `.env` or environment variables.
- Check PyPI for an existing SDK before writing a custom client. Many popular APIs (`stripe`, `openai`, `boto3`) have official libraries.
- If the API requires signup, the skill tells the user and provides the registration URL rather than proceeding without credentials.
- For rate-limited APIs, add `asyncio.sleep()` between requests to stay within limits.
- Always use `httpx` (async) over `requests` (sync) for consistency with async codebases.
