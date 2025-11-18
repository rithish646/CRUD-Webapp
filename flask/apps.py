from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from models import Task, SessionLocal, init_db
from forms import TaskForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'  # change in production

init_db()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.route('/')
def index():
    db = next(get_db())
    tasks = db.query(Task).all()
    return render_template('index.html', tasks=tasks)

@app.route('/task/new', methods=['GET','POST'])
def create_task():
    form = TaskForm()
    if form.validate_on_submit():
        db = next(get_db())
        t = Task(title=form.title.data, description=form.description.data, done=form.done.data)
        db.add(t)
        db.commit()
        flash('Task created', 'success')
        return redirect(url_for('index'))
    return render_template('edit.html', form=form, action='Create')

@app.route('/task/<int:task_id>/edit', methods=['GET','POST'])
def edit_task(task_id):
    db = next(get_db())
    task = db.query(Task).get(task_id)
    if not task:
        flash('Task not found', 'danger')
        return redirect(url_for('index'))
    form = TaskForm(obj=task)
    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        task.done = form.done.data
        db.commit()
        flash('Task updated', 'success')
        return redirect(url_for('index'))
    return render_template('edit.html', form=form, action='Edit')

@app.route('/task/<int:task_id>/delete', methods=['POST'])
def delete_task(task_id):
    db = next(get_db())
    task = db.query(Task).get(task_id)
    if task:
        db.delete(task)
        db.commit()
        flash('Task deleted', 'success')
    return redirect(url_for('index'))

# REST API endpoints
@app.route('/api/tasks', methods=['GET'])
def api_list_tasks():
    db = next(get_db())
    tasks = db.query(Task).all()
    return jsonify([{"id": t.id, "title": t.title, "description": t.description, "done": t.done} for t in tasks])

@app.route('/api/tasks', methods=['POST'])
def api_create_task():
    data = request.json or {}
    db = next(get_db())
    t = Task(title=data.get('title',''), description=data.get('description',''))
    db.add(t)
    db.commit()
    return jsonify({"id": t.id}), 201

if __name__ == '__main__':
    app.run(debug=True)
