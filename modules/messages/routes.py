from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db
from modules.messages.models import Message

messages_bp = Blueprint('messages', __name__, template_folder='templates/messages')

@messages_bp.route('/')
@login_required
def index():
    msgs = Message.query.order_by(Message.timestamp.desc()).all()
    return render_template('messages/index.html', messages=msgs)

@messages_bp.route('/create', methods=['GET','POST'])
@login_required
def create():
    if request.method == 'POST':
        body = request.form['body']
        tag  = request.form.get('tag','')
        m = Message(body=body, tag=tag, user_id=current_user.id)
        db.session.add(m)
        db.session.commit()
        flash('Mesaj gönderildi.', 'success')
        return redirect(url_for('messages.index'))
    return render_template('messages/create.html')

@messages_bp.route('/tag/<tag>')
@login_required
def tag_filter(tag):
    msgs = Message.query.filter_by(tag=tag).all()
    return render_template('messages/index.html', messages=msgs)
