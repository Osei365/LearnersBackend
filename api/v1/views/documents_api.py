from api.v1.views import app_views
from api.v1.views.allquestions import DOCUMENT_FOLDER
from flask import Flask, request, abort, jsonify, send_from_directory


@app_views.route('document/files/<path:filename>')
def get_document(filename):
    """send the directory of the document"""
    return send_from_directory(DOCUMENT_FOLDER, filename, as_attachment=True)