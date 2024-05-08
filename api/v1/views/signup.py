import os
import bcrypt
import uuid
from models import db
from api.v1.views import app_views
from models.teacher import Teacher
from flask import Flask, request, abort, jsonify
from werkzeug.utils import secure_filename

TEACHER_IMAGE_FOLDER = 'app_images/teacher_images/'

@app_views.route('/sign-up', methods=['POST'])
def signup():
    json_doc = request.get_json()
    files = request.files
    if not json_doc:
        abort(404, description='Not a JSON')

    if 'email' not in json_doc:
        abort(404, description='email not present')

    if 'password' not in json_doc:
        abort(404, description='password not present')

    json_doc['password'] = hash_password(json_doc['password'])
    json_doc['email'] = json_doc['email'].lower()
    json_doc['id'] = uuid.uuid4()
    file = files.get('image')
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(TEACHER_IMAGE_FOLDER, filename)
        file.save(filepath)
        json_doc['teacher_image'] = filepath
    teacher = Teacher(**json_doc)
    db.session.add(teacher)
    db.session.commit()
    result = jsonify({"teacherId": "{}".format(json_doc['id']),
                      'isValid': True})
    return result
    
def hash_password(password):
    byte = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(byte, salt)
    return hashed_password
