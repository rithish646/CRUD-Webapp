from fastapi import FastAPI, HTTPException
from sqlmodel import SQLModel, Field, Session, create_engine, select
from typing import Optional

DATABASE_URL = "sqlite:///./tasks_fastapi.db"
engine = create_engine(DATABASE_URL, echo=True)

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = ""
    done: bool = False

app = FastAPI(title="Tasks API")

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

@app.get("/tasks/")
def list_tasks():
    with Session(engine) as session:
        tasks = session.exec(select(Task)).all()
        return tasks

@app.post("/tasks/", status_code=201)
def create_task(task: Task):
    with Session(engine) as session:
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    with Session(engine) as session:
        task = session.get(Task, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return task

@app.put("/tasks/{task_id}")
def update_task(task_id: int, incoming: Task):
    with Session(engine) as session:
        task = session.get(Task, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Not found")
        task.title = incoming.title
        task.description = incoming.description
        task.done = incoming.done
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    with Session(engine) as session:
        task = session.get(Task, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Not found")
        session.delete(task)
        session.commit()
        return None
