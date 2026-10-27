from fastapi import FastAPI, HTTPException
from schemas import TaskCreate, TaskStatusUpdate
from storage import get_tasks, save_task, update_status_task, delete_task, get_clients
from onboarding import show_onboarding, get_onboarding_progress, get_overdue_tasks
from contextlib import asynccontextmanager
from database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="OnboardOps", lifespan=lifespan)


@app.get("/clients/{client_name}/tasks")
def read_tasks(client_name: str):
    tasks = get_tasks(client_name)

    return {"client": client_name, "tasks": tasks}


@app.get("/clients/{client_name}/progress")
def read_onboarding_progress(client_name: str):
    return get_onboarding_progress(client_name)


@app.get("/clients")
def read_clients():
    names = get_clients()
    clients = []

    for name in names:
        progress = get_onboarding_progress(name)
        clients.append({"name": name, "progress_percent": progress["progress_percent"]})

    return {"clients": clients}


@app.get("/clients/{client_name}/overdue")
def read_overdue_tasks(client_name: str):
    overdue_tasks = get_overdue_tasks(client_name)
    return overdue_tasks


@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    created = save_task(task.model_dump(mode="json"))
    if created is False:
        raise HTTPException(status_code=409, detail="Task already exists")
    return task


@app.patch("/clients/{client_name}/tasks/{title}")
def update_task(client_name: str, title: str, changes: TaskStatusUpdate):
    updated = update_status_task(client_name, title, changes.status)
    if not updated:
        raise HTTPException(status_code=404, detail="Task not found")
    else:
        return {"updated": updated}


@app.delete("/clients/{client_name}/tasks/{title}")
def remove_task(client_name: str, title: str):
    deleted = delete_task(client_name, title)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    else:
        return {"deleted": deleted}


@app.post("/clients/{client_name}/onboarding")
def create_onboarding(client_name: str):
    tasks = show_onboarding(client_name)
    for task in tasks:
        save_task(task)
    return get_tasks(client_name)
