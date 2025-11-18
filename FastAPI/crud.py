from sqlmodel import Session, select
from models import Task
from schemas import TaskCreate, TaskUpdate

def get_all_tasks(session: Session):
    return session.exec(select(Task)).all()

def get_task(session: Session, task_id: int):
    return session.get(Task, task_id)

def create_task(session: Session, data: TaskCreate):
    task = Task(
        title=data.title,
        description=data.description,
        done=data.done,
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

def update_task(session: Session, task_id: int, data: TaskUpdate):
    task = session.get(Task, task_id)
    if not task:
        return None

    for field, value in data.dict(exclude_unset=True).items():
        setattr(task, field, value)

    session.add(task)
    session.commit()
    session.refresh(task)
    return task

def delete_task(session: Session, task_id: int):
    task = session.get(Task, task_id)
    if not task:
        return None

    session.delete(task)
    session.commit()
    return True
