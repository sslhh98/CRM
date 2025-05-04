from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user
from modules.messages.models import Message
from extensions import db
from modules.dashboard.models import Activity

messages_bp = Blueprint('messages', __name__, url_prefix='/messages')

@messages_bp.route('/', methods=['GET'], endpoint='index')
def index():
    msgs = Message.query.order_by(Message.timestamp.desc()).all()
    return render_template('messages_list.html', messages=msgs)

@messages_bp.route('/add', methods=['GET','POST'], endpoint='add_message')
def add_message():
    if request.method=='POST':
        body = request.form.get('body','').strip()
        tag  = request.form.get('tag','').lstrip('#').strip()
        if body:
            m = Message(body=body, tag=tag)
            db.session.add(m)
            db.session.commit()
            # Activity kaydı
            act = Activity(
                user_id=current_user.id,
                customer_id=None,
                action=f"Yeni mesaj: “{body[:20]}…” eklendi."
            )
            db.session.add(act)
            db.session.commit()
        return redirect(url_for('messages.index'))
    return render_template('add_message.html')

@messages_bp.route('/delete/<int:message_id>', endpoint='delete_message')
def delete_message(message_id):
    m = Message.query.get_or_404(message_id)
    snippet = m.body[:20]
    db.session.delete(m)
    db.session.commit()
    # Activity kaydı
    act = Activity(
        user_id=current_user.id,
        customer_id=None,
        action=f"Mesaj “{snippet}…” silindi."
    )
    db.session.add(act)
    db.session.commit()
    return redirect(url_for('messages.index'))
