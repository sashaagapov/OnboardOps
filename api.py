from fastapi import FastAPI, HTTPException
from schemas import TaskCreate, TaskStatusUpdate
from storage import get_tasks, save_task, update_status_task, delete_task
from onboarding import show_onboarding

app = FastAPI(title="OnboardOps")


@app.get("/clients/{client_name}/tasks")
def read_tasks(client_name: str):
    tasks = get_tasks(client_name)

    return {"client": client_name, "tasks": tasks}


@app.post("/tasks")
def create_task(task: TaskCreate):
    save_task(task.model_dump())
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
    return {"client": client_name, "tasks": tasks}
