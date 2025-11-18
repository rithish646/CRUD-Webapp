from typing import Optional
from pydantic import BaseModel

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = ""
    done: bool = False

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    done: Optional[bool] = None

class TaskRead(BaseModel):
    id: int
    title: str
    description: Optional[str]
    done: bool

    class Config:
        orm_mode = True
