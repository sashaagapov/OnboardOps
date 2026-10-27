from pydantic import BaseModel
from datetime import date
from typing import Literal 

class TaskCreate(BaseModel):
    client: str
    title: str
    status: Literal["pending","completed"] = "pending"
    due_date: date | None = None 

class TaskStatusUpdate(BaseModel):
    status : Literal["pending","completed"]