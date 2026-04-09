from typing import Dict, Generator

import pytest

from app.main import MOCK_TASKS, fetch_all_tasks, generate_productivity_report
from app.models import DeveloperTask, TaskStatus


@pytest.fixture(autouse=True)
def restore_mock_tasks() -> Generator[None, None, None]:
    original: Dict[int, DeveloperTask] = dict(MOCK_TASKS)
    yield
    MOCK_TASKS.clear()
    MOCK_TASKS.update(original)


@pytest.mark.asyncio
async def test_fetch_all_tasks_returns_list() -> None:
    tasks = await fetch_all_tasks()

    assert isinstance(tasks, list)
    assert all(isinstance(t, DeveloperTask) for t in tasks)


@pytest.mark.asyncio
async def test_fetch_all_tasks_count_matches_mock() -> None:
    tasks = await fetch_all_tasks()

    assert len(tasks) == len(MOCK_TASKS)


@pytest.mark.asyncio
async def test_fetch_all_tasks_empty_when_no_tasks() -> None:
    MOCK_TASKS.clear()
    tasks = await fetch_all_tasks()

    assert tasks == []


@pytest.mark.asyncio
async def test_generate_report_completion_rate_calculation() -> None:
    MOCK_TASKS.clear()
    MOCK_TASKS[1] = DeveloperTask(task_id=1, title="Task A", status=TaskStatus.COMPLETE, hours_spent=5.0)
    MOCK_TASKS[2] = DeveloperTask(task_id=2, title="Task B", status=TaskStatus.COMPLETE, hours_spent=5.0)
    MOCK_TASKS[3] = DeveloperTask(task_id=3, title="Task C", status=TaskStatus.PENDING, hours_spent=0.0)
    MOCK_TASKS[4] = DeveloperTask(task_id=4, title="Task D", status=TaskStatus.PENDING, hours_spent=0.0)

    report = await generate_productivity_report()

    assert report.total_tasks == 4
    assert report.completed_tasks == 2
    assert report.completion_rate == 50.0


@pytest.mark.asyncio
async def test_generate_report_zero_division_handled() -> None:
    MOCK_TASKS.clear()

    report = await generate_productivity_report()

    assert report.completion_rate == 0.0
    assert report.total_tasks == 0


@pytest.mark.asyncio
async def test_generate_report_total_hours_summed_correctly() -> None:
    MOCK_TASKS.clear()
    MOCK_TASKS[1] = DeveloperTask(task_id=1, title="Task A", status=TaskStatus.COMPLETE, hours_spent=3.5)
    MOCK_TASKS[2] = DeveloperTask(task_id=2, title="Task B", status=TaskStatus.PENDING, hours_spent=1.5)

    report = await generate_productivity_report()

    assert report.total_hours_spent == 5.0