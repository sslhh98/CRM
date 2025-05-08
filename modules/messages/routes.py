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

# modules/messages/routes.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from extensions import db
from .models import Message

messages_bp = Blueprint('messages', __name__)

@messages_bp.route('/')
def index():
    msgs = Message.query.order_by(Message.created_at.desc()).all()
    return render_template('messages_list.html', messages=msgs)

@messages_bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        body = request.form['body'].strip()
        m = Message(body=body)
        db.session.add(m)
        db.session.commit()
        flash('Mesaj eklendi.', 'success')
        return redirect(url_for('messages.index'))
    return render_template('add_message.html')

@messages_bp.route('/tag/<tag>')
def tag_filter(tag):
    msgs = Message.query.filter(Message.body.contains(f"#{tag}")).all()
    return render_template('search_results.html', messages=msgs, query=f"#{tag}")
