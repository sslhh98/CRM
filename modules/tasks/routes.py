from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user
from sqlalchemy.exc import IntegrityError
from modules.tasks.models import Task
from extensions import db
from datetime import datetime
from modules.dashboard.models import Activity

tasks_bp = Blueprint('tasks', __name__, url_prefix='/tasks')

# modules/tasks/routes.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from extensions import db
from .models import Task

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/')
def index():
    tasks = Task.query.order_by(Task.due_date).all()
    return render_template('tasks_list.html', tasks=tasks)

@tasks_bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form['title'].strip()
        due   = request.form['due_date']
        t = Task(title=title, due_date=due)
        db.session.add(t)
        db.session.commit()
        flash('Görev eklendi.', 'success')
        return redirect(url_for('tasks.index'))
    return render_template('add_task.html')

@tasks_bp.route('/<int:id>/complete', methods=['POST'])
def complete(id):
    t = Task.query.get_or_404(id)
    t.completed = True
    db.session.commit()
    flash('Görev tamamlandı.', 'info')
    return redirect(url_for('tasks.index'))
