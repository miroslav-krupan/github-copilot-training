import pytest
from httpx import AsyncClient
from app.main import app, MOCK_TASKS
from app.models import DeveloperTask, TaskStatus


@pytest.mark.asyncio
async def test_get_status() -> None:
    """Test /status endpoint returns ok status."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/status")
    
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_get_all_tasks() -> None:
    """Test /tasks endpoint returns all tasks."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/tasks")
    
    assert response.status_code == 200
    tasks = response.json()
    assert isinstance(tasks, list)
    assert len(tasks) == 3


@pytest.mark.asyncio
async def test_get_productivity_report() -> None:
    """Test /report endpoint returns correct productivity metrics."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/report")
    
    assert response.status_code == 200
    report = response.json()
    
    assert report["total_tasks"] == 3
    assert report["completed_tasks"] == 1
    assert report["completion_rate"] == 33.33
    assert "total_hours_spent" in report


@pytest.mark.asyncio
async def test_log_task() -> None:
    """Test /log_task endpoint creates and stores a new task."""
    new_task = {
        "task_id": 99,
        "title": "Test task",
        "status": "pending",
        "hours_spent": 2.5
    }
    
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/log_task", json=new_task)
    
    assert response.status_code == 200
    result = response.json()
    assert "task_id" in result
    assert result["message"] == "Task logged successfully."
    assert isinstance(result["task_id"], int)
