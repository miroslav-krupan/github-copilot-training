---
description: "Global rules for generating and updating tests in this repository."
applyTo: "tests/**/*.py"
---

# Test Generation Guidelines

## Framework
- Use `pytest`.
- Use `pytest-asyncio` for async tests.
- Use `httpx.AsyncClient` with `ASGITransport` for FastAPI endpoint tests.

## Naming Conventions
- Test file names: `test_<module_or_feature>.py`
- Test function names: `test_<behavior>_<expected_result>`
- Optional class names: `Test<FeatureName>`

## Preferred Folder Structure
- `tests/conftest.py` for shared fixtures
- `tests/unit/` for unit tests
- `tests/integration/` for endpoint/integration tests

## Required Fixtures
- Reuse shared fixtures from `tests/conftest.py`:
  - `async_client`
  - `sample_task_payload`

## Coverage Expectations
For every new/changed endpoint or utility:
- Happy path
- Validation/bad input path
- Failure/error path (e.g., 404)

## Templates

### Endpoint test template
````python
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_<endpoint_behavior>(async_client: AsyncClient) -> None:
    response = await async_client.get("/path")
    assert response.status_code == 200
    body = response.json()
    assert "key" in body