from flask import Blueprint, render_template, request, redirect, url_for
from modules.messages.models import Message
from extensions import db

messages_bp = Blueprint('messages', __name__)

# Ana liste + link “Yeni Mesaj” sayfasına
@messages_bp.route('/', methods=['GET'], endpoint='index')
def index():
    msgs = Message.query.order_by(Message.timestamp.desc()).all()
    return render_template('messages_list.html', messages=msgs)

# “Yeni Mesaj” formu
@messages_bp.route('/add', methods=['GET', 'POST'], endpoint='add_message')
def add_message():
    if request.method == 'POST':
        body = request.form.get('body', '').strip()
        tag  = request.form.get('tag', '').lstrip('#').strip()
        if body:
            m = Message(body=body, tag=tag)
            db.session.add(m)
            db.session.commit()
        return redirect(url_for('messages.index'))
    return render_template('add_message.html')

# Silme işlemi
@messages_bp.route('/delete/<int:message_id>', endpoint='delete_message')
def delete_message(message_id):
    m = Message.query.get_or_404(message_id)
    db.session.delete(m)
    db.session.commit()
    return redirect(url_for('messages.index'))
