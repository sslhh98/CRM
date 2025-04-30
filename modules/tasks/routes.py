from flask import Blueprint, render_template, request, redirect, url_for, flash
from modules.tasks.models import Task
from extensions import db
from sqlalchemy.exc import IntegrityError
from datetime import datetime

tasks_bp = Blueprint('tasks', __name__)

# Listeleme + Arama + Yeni görev ekleme
@tasks_bp.route('/', methods=['GET','POST'], endpoint='index')
def index():
    if request.method == 'POST':
        title = request.form.get('title','').strip()
        desc  = request.form.get('description','').strip()
        due   = request.form.get('due_date','').strip()

        if not title:
            flash("Lütfen görev başlığını girin.", "error")
            return redirect(url_for('tasks.index'))

        task = Task(title=title,
                    description=desc,
                    status='Beklemede',
                    due_date=(datetime.strptime(due, '%Y-%m-%d')
                              if due else None))
        db.session.add(task)
        try:
            db.session.commit()
            flash("Yeni görev eklendi.", "success")
        except IntegrityError:
            db.session.rollback()
            flash("Görev eklenirken bir hata oluştu.", "error")

        return redirect(url_for('tasks.index'))

    # GET: arama varsa filtrele
    q = request.args.get('q','').strip()
    if q:
        tasks = (Task.query
                 .filter(
                   (Task.title.contains(q)) |
                   (Task.description.contains(q))
                 )
                 .order_by(Task.created_at.desc())
                 .all())
    else:
        tasks = Task.query.order_by(Task.created_at.desc()).all()

    return render_template('tasks_index.html', tasks=tasks, search=q)

# Görev durumu güncelleme
@tasks_bp.route('/update/<int:id>', methods=['POST'], endpoint='update_task')
def update_task(id):
    task = Task.query.get_or_404(id)
    new_status = request.form.get('status')
    if new_status in ('Beklemede','Devam','Tamamlandı'):
        task.status = new_status
        db.session.commit()
        flash("Görev durumu güncellendi.", "success")
    return redirect(url_for('tasks.index'))

# Görev silme
@tasks_bp.route('/delete/<int:id>', endpoint='delete_task')
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    flash("Görev silindi.", "success")
    return redirect(url_for('tasks.index'))
