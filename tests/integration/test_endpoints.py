from typing import Dict

import pytest
from httpx import AsyncClient

from app.main import MOCK_TASKS
from app.models import DeveloperTask, TaskStatus


@pytest.fixture(autouse=True)
def restore_mock_tasks() -> None:
    original: Dict[int, DeveloperTask] = dict(MOCK_TASKS)
    yield
    MOCK_TASKS.clear()
    MOCK_TASKS.update(original)


@pytest.mark.asyncio
async def test_status_endpoint_returns_ok(async_client: AsyncClient) -> None:
    response = await async_client.get("/status")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_tasks_endpoint_returns_all_tasks(async_client: AsyncClient) -> None:
    response = await async_client.get("/tasks")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 3


@pytest.mark.asyncio
async def test_tasks_endpoint_returns_empty_list_when_no_tasks(async_client: AsyncClient) -> None:
    MOCK_TASKS.clear()
    response = await async_client.get("/tasks")

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_report_endpoint_returns_correct_metrics(async_client: AsyncClient) -> None:
    response = await async_client.get("/report")

    assert response.status_code == 200
    data = response.json()
    assert data["total_tasks"] == 3
    assert data["completed_tasks"] == 1
    assert data["total_hours_spent"] == 23.5
    assert data["completion_rate"] == 33.33


@pytest.mark.asyncio
async def test_report_endpoint_empty_tasks(async_client: AsyncClient) -> None:
    MOCK_TASKS.clear()
    response = await async_client.get("/report")

    assert response.status_code == 200
    data = response.json()
    assert data["total_tasks"] == 0
    assert data["completion_rate"] == 0.0


@pytest.mark.asyncio
async def test_task_status_endpoint_success(async_client: AsyncClient) -> None:
    response = await async_client.get("/task/1/status")

    assert response.status_code == 200
    assert response.json() == {"task_id": 1, "status": "complete"}


@pytest.mark.asyncio
async def test_task_status_endpoint_in_progress(async_client: AsyncClient) -> None:
    response = await async_client.get("/task/2/status")

    assert response.status_code == 200
    assert response.json()["status"] == "in_progress"


@pytest.mark.asyncio
async def test_task_status_endpoint_pending(async_client: AsyncClient) -> None:
    response = await async_client.get("/task/3/status")

    assert response.status_code == 200
    assert response.json()["status"] == "pending"


@pytest.mark.asyncio
async def test_task_status_endpoint_not_found(async_client: AsyncClient) -> None:
    response = await async_client.get("/task/999/status")

    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}


@pytest.mark.asyncio
async def test_task_status_endpoint_invalid_id_type(async_client: AsyncClient) -> None:
    response = await async_client.get("/task/abc/status")

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_task_status_endpoint_negative_id_not_found(async_client: AsyncClient) -> None:
    response = await async_client.get("/task/-1/status")

    assert response.status_code == 404