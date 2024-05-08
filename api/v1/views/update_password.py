import bcrypt
import os
from models import db
from models.teacher import Teacher
from api.v1.views import app_views
from flask import Flask, request, abort, jsonify
from api.v1.views.signup import hash_password
from flask_mail import Mail, Message


mail_username = os.getenv('mail_username')

@app_views.route('update-password/<teacher_id>', methods=['PUT'])
def update_password(teacher_id):
    """updates the password of the Teacher"""

    passwords = request.get_json()
    if not passwords:
        abort(400)

    initial_password = passwords.get('initialPassword')
    if not initial_password:
        abort(400)
    new_password = passwords.get('newPassword')
    if not new_password:
        abort(400)

    teacher = db.get_or_404(Teacher, teacher_id)
    if bcrypt.checkpw(initial_password.encode('utf-8'), teacher.password.encode('utf-8')):
        teacher.password = hash_password(new_password)
        db.session.commit()
    else:
        abort(404, description='incorrect password')

    return jsonify({'status': 'successful'})

@app_views.route('send-email/<teacher_id>', methods=['POST'])
def send_email(teacher_id):
    """sends reset password link to email"""
    from app import mail

    data = request.get_json()
    if not data:
        abort(400)

    recipient_email = data.get('email')
    message = Message(subject='Change Password', sender=mail_username, recipients=[recipient_email])
    message.body = 'Testing'
    mail.send(message)

    return jsonify({'status': 'email sent successfully'})

