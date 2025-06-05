from flask import Blueprint

from ..blueprints.user import user_bp
from ..blueprints.photo import photo_bp

api_bp = Blueprint('api', __name__)

api_bp.register_blueprint(user_bp, url_prefix='/user')
api_bp.register_blueprint(photo_bp, url_prefix='/photo')
