# modules/messages/routes.py
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user
from modules.messages.models import Message
from extensions import db, log_activity

messages_bp = Blueprint('messages', __name__, url_prefix='/messages')

@messages_bp.route('/', methods=['GET'], endpoint='index')
def index():
    msgs = Message.query.order_by(Message.timestamp.desc()).all()
    return render_template('messages_list.html', messages=msgs)

@messages_bp.route('/add', methods=['GET','POST'], endpoint='add_message')
def add_message():
    if request.method == 'POST':
        body = request.form.get('body','').strip()
        tag  = request.form.get('tag','').lstrip('#').strip()
        if body:
            msg = Message(body=body, tag=tag)
            db.session.add(msg)
            db.session.commit()

            log_activity(
                user_id=current_user.id,
                module_name='messages',
                action=f'Yeni mesaj: “{body[:20]}…” eklendi.',
                item_id=msg.id
            )
        return redirect(url_for('messages.index'))
    return render_template('add_message.html')

@messages_bp.route('/edit/<int:message_id>', methods=['GET','POST'], endpoint='edit_message')
def edit_message(message_id):
    msg = Message.query.get_or_404(message_id)
    if request.method == 'POST':
        old_body = msg.body
        msg.body = request.form.get('body','').strip()
        msg.tag  = request.form.get('tag','').lstrip('#').strip()
        db.session.commit()

        log_activity(
            user_id=current_user.id,
            module_name='messages',
            action=(
                f'Mesaj {message_id} güncellendi: '
                f'“{old_body[:20]}…” → “{msg.body[:20]}…”'
            ),
            item_id=message_id
        )
        return redirect(url_for('messages.index'))
    return render_template('edit_message.html', message=msg)

@messages_bp.route('/delete/<int:message_id>', methods=['POST'], endpoint='delete_message')
def delete_message(message_id):
    msg = Message.query.get_or_404(message_id)
    snippet = msg.body[:20]
    db.session.delete(msg)
    db.session.commit()

    log_activity(
        user_id=current_user.id,
        module_name='messages',
        action=f'Mesaj “{snippet}…” silindi.',
        item_id=message_id
    )
    return redirect(url_for('messages.index'))
