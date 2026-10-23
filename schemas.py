
from pydantic import BaseModel


class TaskCreate(BaseModel):
    client: str
    title: str
    status: str = "pending"

class TaskStatusUpdate(BaseModel):
    status : str