from flask import Blueprint, jsonify
from werkzeug.exceptions import HTTPException

errors_bp = Blueprint('errors_bp', __name__)

@errors_bp.app_errorhandler(HTTPException)
def handle_exception(e):
    return jsonify({
        "error": e.name,
        "message": e.description
    }), e.code