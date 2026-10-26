from pydantic import BaseModel
from datetime import date

class TaskCreate(BaseModel):
    client: str
    title: str
    status: str = "pending"
    due_date: date | None = None 

class TaskStatusUpdate(BaseModel):
    status : str