from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user
from sqlalchemy.exc import IntegrityError
from modules.tasks.models import Task
from extensions import db
from datetime import datetime
from modules.dashboard.models import Activity

tasks_bp = Blueprint('tasks', __name__, url_prefix='/tasks')

@tasks_bp.route('/', methods=['GET','POST'], endpoint='index')
def index():
    if request.method=='POST':
        title = request.form.get('title','').strip()
        desc  = request.form.get('description','').strip()
        due   = request.form.get('due_date','').strip()

        if not title:
            flash("Lütfen görev başlığını girin.", "error")
            return redirect(url_for('tasks.index'))

        task = Task(
            title=title,
            description=desc,
            status='Beklemede',
            due_date=(datetime.strptime(due,'%Y-%m-%d') if due else None)
        )
        db.session.add(task)
        try:
            db.session.commit()
            # Activity kaydı
            act = Activity(
                user_id=current_user.id,
                customer_id=task.customer_id,
                action=f"Yeni görev “{task.title}” eklendi."
            )
            db.session.add(act)
            db.session.commit()

            flash("Yeni görev eklendi.", "success")
        except IntegrityError:
            db.session.rollback()
            flash("Görev eklenirken bir hata oluştu.", "error")
        return redirect(url_for('tasks.index'))

    q = request.args.get('q','').strip()
    if q:
        tasks = Task.query.filter(
            (Task.title.contains(q)) |
            (Task.description.contains(q))
        ).order_by(Task.created_at.desc()).all()
    else:
        tasks = Task.query.order_by(Task.created_at.desc()).all()

    return render_template('tasks_index.html', tasks=tasks, search=q)


@tasks_bp.route('/update/<int:id>', methods=['POST'], endpoint='update_task')
def update_task(id):
    task = Task.query.get_or_404(id)
    new_status = request.form.get('status')
    if new_status in ('Beklemede','Devam','Tamamlandı'):
        task.status = new_status
        db.session.commit()
        # Activity kaydı
        act = Activity(
            user_id=current_user.id,
            customer_id=task.customer_id,
            action=f"Görev “{task.title}” durumu “{new_status}” yapıldı."
        )
        db.session.add(act)
        db.session.commit()

        flash("Görev durumu güncellendi.", "success")
    return redirect(url_for('tasks.index'))


@tasks_bp.route('/delete/<int:id>', endpoint='delete_task')
def delete_task(id):
    task = Task.query.get_or_404(id)
    title = task.title
    db.session.delete(task)
    db.session.commit()
    # Activity kaydı
    act = Activity(
        user_id=current_user.id,
        customer_id=task.customer_id,
        action=f"Görev “{title}” silindi."
    )
    db.session.add(act)
    db.session.commit()

    flash("Görev silindi.", "success")
    return redirect(url_for('tasks.index'))
