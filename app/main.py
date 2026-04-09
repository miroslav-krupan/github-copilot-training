from typing import Dict, List, Any
import asyncio
from fastapi import FastAPI

from app.models import TaskStatus, DeveloperTask, ProductivityReport


# --- Mock Database / In-Memory Service Logic
MOCK_TASKS: Dict[int, DeveloperTask] = {
    1: DeveloperTask(task_id=1, title="Refactor legacy service", status=TaskStatus.COMPLETE, hours_spent=8.5),
    2: DeveloperTask(task_id=2, title="Implement new user auth flow", status=TaskStatus.IN_PROGRESS, hours_spent=15.0),
    3: DeveloperTask(task_id=3, title="Write unit tests for checkout", status=TaskStatus.PENDING, hours_spent=0.0),
}

# Simulate asynchronous I/O with a slight delay
async def fetch_all_tasks() -> List[DeveloperTask]:
    """Simulates fetching all tasks asynchronously."""
    await asyncio.sleep(0.01)
    return list(MOCK_TASKS.values())

async def generate_productivity_report() -> ProductivityReport:
    """Calculates key metrics based on all tasks."""
    tasks = await fetch_all_tasks()
    
    total_tasks = len(tasks)
    completed_tasks = sum(1 for task in tasks if task.status == TaskStatus.COMPLETE)
    
    total_hours_spent = sum(task.hours_spent for task in tasks)
    completion_rate = round((completed_tasks / total_tasks) * 100, 2) if total_tasks > 0 else 0.0
    
    return ProductivityReport(
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        total_hours_spent=round(total_hours_spent, 2),
        completion_rate=completion_rate
    )


# --- FastAPI Initialization and Routes ---
app = FastAPI(title="Productivity Reporting System")

@app.get("/status")
async def get_status() -> Dict[str, str]:
    return {"status": "ok"}


@app.get("/tasks", response_model=List[DeveloperTask])
async def get_all_tasks():
    """Returns a list of all logged tasks."""
    return await fetch_all_tasks()


@app.get("/report", response_model=ProductivityReport)
async def get_productivity_report():
    """Returns the calculated productivity report."""
    return await generate_productivity_report()


@app.post("/log_task")
async def log_task(task: DeveloperTask) -> Dict[str, Any]:
    """Creates a new task entry, assigns it a new ID, and returns a confirmation payload."""
    new_id = max(MOCK_TASKS.keys()) + 1 if MOCK_TASKS else 1
    new_task = task.model_copy(update={"task_id": new_id})
    MOCK_TASKS[new_id] = new_task
    
    return {"task_id": new_task.task_id, "message": "Task logged successfully."}


@app.get("/task/{task_id}/status")
async def get_task_status(task_id: int) -> Dict[str, str]:
    """Returns the status of a specific task by its ID."""
    task = MOCK_TASKS.get(task_id)
    if not task:
        return {"error": "Task not found"}
    
    return {"task_id": task_id, "status": task.status.value}