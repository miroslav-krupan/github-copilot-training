from typing import Dict

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import (
    MOCK_TASKS,
    app,
    fetch_all_tasks,
    generate_productivity_report,
    get_all_tasks,
    get_productivity_report,
    get_status,
    get_task_status,
)
from app.models import TaskStatus


@pytest.fixture(autouse=True)
def restore_mock_tasks() -> None:
    """Keep MOCK_TASKS isolated per test."""
    original: Dict[int, object] = dict(MOCK_TASKS)
    yield
    MOCK_TASKS.clear()
    MOCK_TASKS.update(original)


@pytest.mark.asyncio
async def test_fetch_all_tasks_returns_all_tasks() -> None:
    tasks = await fetch_all_tasks()

    assert len(tasks) == 3
    assert tasks[0].task_id == 1
    assert tasks[1].status == TaskStatus.IN_PROGRESS
    assert tasks[2].title == "Write unit tests for checkout"


@pytest.mark.asyncio
async def test_generate_productivity_report_returns_expected_metrics() -> None:
    report = await generate_productivity_report()

    assert report.total_tasks == 3
    assert report.completed_tasks == 1
    assert report.total_hours_spent == 23.5
    assert report.completion_rate == 33.33


@pytest.mark.asyncio
async def test_generate_productivity_report_handles_empty_tasks() -> None:
    MOCK_TASKS.clear()

    report = await generate_productivity_report()

    assert report.total_tasks == 0
    assert report.completed_tasks == 0
    assert report.total_hours_spent == 0.0
    assert report.completion_rate == 0.0


@pytest.mark.asyncio
async def test_get_status_function() -> None:
    result = await get_status()
    assert result == {"status": "ok"}


@pytest.mark.asyncio
async def test_get_all_tasks_function() -> None:
    result = await get_all_tasks()
    assert len(result) == 3


@pytest.mark.asyncio
async def test_get_productivity_report_function() -> None:
    result = await get_productivity_report()
    assert result.completion_rate == 33.33


@pytest.mark.asyncio
async def test_get_task_status_function_success() -> None:
    result = await get_task_status(1)
    assert result == {"task_id": 1, "status": "complete"}


@pytest.mark.asyncio
async def test_status_endpoint() -> None:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/status")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_tasks_endpoint() -> None:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/tasks")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 3


@pytest.mark.asyncio
async def test_report_endpoint() -> None:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/report")

    assert response.status_code == 200
    assert response.json()["completion_rate"] == 33.33


@pytest.mark.asyncio
async def test_task_status_endpoint_success() -> None:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/task/1/status")

    assert response.status_code == 200
    assert response.json() == {"task_id": 1, "status": "complete"}


@pytest.mark.asyncio
async def test_task_status_endpoint_not_found() -> None:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/task/999/status")

    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}
