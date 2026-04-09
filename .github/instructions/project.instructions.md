---
description: "Use when editing FastAPI application files, route handlers, service logic, or Pydantic-backed API code in this training project. Covers async endpoints, type hints, model placement, and response conventions."
applyTo: "app/**/*.py"
---
# FastAPI Project Guidelines

- Use `async def` for all route handlers and I/O-bound functions, and `await` asynchronous calls.
- Add explicit type hints to every function parameter and return value.
- Keep all Pydantic models and API enums in `app/models.py`; import them into route modules instead of redefining them.
- Return standard Python dictionaries, lists, or Pydantic models from endpoints. Do not return raw strings.
- Keep application logic in `app/` focused and minimal; prefer small helpers over embedding complex logic directly in route handlers.
- When adding or changing endpoints or utility functions, add or update tests under `tests/` and follow the testing rules in `.github/instructions/unit-test.instructions.md`.