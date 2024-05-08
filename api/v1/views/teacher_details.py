import os
from models import db
from models.teacher import Teacher
from flask import request, jsonify, abort
from api.v1.views import app_views
from werkzeug.utils import secure_filename
from api.v1.views.signup import TEACHER_IMAGE_FOLDER


@app_views.route('/teacher-details/<teacher_id>')
def teacher_details(teacher_id):
    """return teacher details"""

    teacher = db.get_or_404(Teacher, teacher_id)

    result = {}
    result['first_name'] = teacher.first_name
    result['last_name'] = teacher.last_name
    result['email'] = teacher.email
    if teacher.teacher_image:
        result['teacher_image'] = teacher.teacher_image
    return jsonify(result)

@app_views.route('/save-teacherimage/<teacher_id>', methods=['PUT'])
def save_teacherimage(teacher_id):
    """saves the teacher's new image"""
    files = request.files
    if not files:
        abort(400, description='image of teacher is missing')

    teacher = db.get_or_404(Teacher, teacher_id )
    file = files.get('image')
    print(file)
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(TEACHER_IMAGE_FOLDER, filename)
        file.save(filepath)
        if teacher.teacher_image:
            if os.path.exists(teacher.teacher_image):
                os.remove(teacher.teacher_image)
        teacher.teacher_image = filepath
        db.session.commit()
    else:
        abort(400, description='it is not a file')

    return jsonify({'status_code': 'Profile updated successfully',
                    'teacherImage': filepath})
