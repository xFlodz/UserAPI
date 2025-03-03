from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..services.tag_service import (
    create_tag_service,
    delete_tag_service,
    get_all_tags_service
)

tag_bp = Blueprint('tag', __name__)


@tag_bp.route('/create', methods=['POST'])
@jwt_required(refresh=True)
def create_tag():
    data = request.json
    current_user_email = get_jwt_identity()

    return create_tag_service(data, current_user_email)



@tag_bp.route('/delete/<int:tag_id>', methods=['DELETE'])
@jwt_required(refresh=True)
def delete_tag(tag_id):
    current_user_email = get_jwt_identity()

    return delete_tag_service(tag_id, current_user_email)


@tag_bp.route('/get_all_tags', methods=['GET'])
def get_all_tags():
    return get_all_tags_service()

