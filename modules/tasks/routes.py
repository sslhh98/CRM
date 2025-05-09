from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db
from modules.tasks.models import Task

tasks_bp = Blueprint('tasks', __name__, template_folder='templates/tasks')

@tasks_bp.route('/')
@login_required
def index():
    tasks = Task.query.order_by(Task.due_date).all()
    return render_template('tasks/index.html', tasks=tasks)

@tasks_bp.route('/create', methods=['GET','POST'])
@login_required
def create():
    if request.method == 'POST':
        title   = request.form['title']
        due_date= request.form['due_date']  # yyyy-mm-dd
        t = Task(title=title, due_date=due_date, user_id=current_user.id)
        db.session.add(t)
        db.session.commit()
        flash('Görev oluşturuldu.', 'success')
        return redirect(url_for('tasks.index'))
    return render_template('tasks/create.html')

@tasks_bp.route('/<int:id>/toggle')
@login_required
def toggle(id):
    t = Task.query.get_or_404(id)
    t.completed = not t.completed
    db.session.commit()
    return redirect(url_for('tasks.index'))
