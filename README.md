# Full CRUD Web Application

A small full-stack CRUD web application implemented with both **Flask** and **FastAPI** (choose one to present).  
Implements a `Task` resource with create, read, update, delete operations backed by SQLite.

## Features
- RESTful endpoints for Tasks (JSON)
- Simple web UI for Flask implementation (create/edit/list)
- FastAPI implementation includes automatic OpenAPI docs
- SQLite + SQLAlchemy/SQLModel for persistence
- Dockerfile + docker-compose for easy running
- GitHub Actions CI for linting and testing

## Tech stack
- Python 3.10+
- Flask + SQLAlchemy (flask/)
- FastAPI + SQLModel (fastapi/)
- SQLite for lightweight persistence
- Docker (optional)

## How to run (Flask)
```bash
cd flask
python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python app.py
# visit http://127.0.0.1:5000

