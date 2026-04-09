import pytest
from pydantic import ValidationError

from app.models import DeveloperTask, ProductivityReport, TaskStatus


def test_developer_task_valid_creation() -> None:
    task = DeveloperTask(task_id=1, title="Fix bug", status=TaskStatus.PENDING, hours_spent=2.0)

    assert task.task_id == 1
    assert task.title == "Fix bug"
    assert task.status == TaskStatus.PENDING
    assert task.hours_spent == 2.0


def test_developer_task_missing_title_raises_error() -> None:
    with pytest.raises(ValidationError):
        DeveloperTask(task_id=1, status=TaskStatus.PENDING, hours_spent=2.0)  # type: ignore


def test_developer_task_invalid_status_raises_error() -> None:
    with pytest.raises(ValidationError):
        DeveloperTask(task_id=1, title="Fix bug", status="invalid_status", hours_spent=2.0)  # type: ignore


def test_productivity_report_valid_creation() -> None:
    report = ProductivityReport(
        total_tasks=5,
        completed_tasks=2,
        total_hours_spent=10.0,
        completion_rate=40.0,
    )

    assert report.total_tasks == 5
    assert report.completed_tasks == 2
    assert report.total_hours_spent == 10.0
    assert report.completion_rate == 40.0


def test_productivity_report_missing_field_raises_error() -> None:
    with pytest.raises(ValidationError):
        ProductivityReport(total_tasks=5, completed_tasks=2, total_hours_spent=10.0)  # type: ignore


def test_task_status_enum_values() -> None:
    assert TaskStatus.PENDING == "pending"
    assert TaskStatus.IN_PROGRESS == "in_progress"
    assert TaskStatus.COMPLETE == "complete"