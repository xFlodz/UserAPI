from flask import Blueprint

from ..blueprints.user import user_bp
from ..blueprints.post import post_bp
from ..blueprints.file import file_bp
from ..blueprints.tag import tag_bp

api_bp = Blueprint('api', __name__)

api_bp.register_blueprint(user_bp, url_prefix='/user')
api_bp.register_blueprint(post_bp, url_prefix='/post')
api_bp.register_blueprint(file_bp, url_prefix='/file')
api_bp.register_blueprint(tag_bp, url_prefix='tag')
