from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.services.user_service import register_user, login_user, refresh_token, logout_user_service, get_adm, add_editor_service, get_all_editors, delete_editor_service

user_bp = Blueprint('user', __name__)


@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    return register_user(data)


@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    return login_user(data)


@user_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    return refresh_token()


@user_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    current_user_email = get_jwt_identity()
    return logout_user_service(current_user_email)


@user_bp.route('/add_editor', methods=['POST'])
@jwt_required()
def add_editor():
    current_user_email = get_jwt_identity()
    data = request.get_json()
    print(data['email'])

    return add_editor_service(data['email'], current_user_email)


@user_bp.route('/get_editors', methods=['GET'])
@jwt_required()
def get_editors():
    current_user_email = get_jwt_identity()
    return get_all_editors(current_user_email)


@user_bp.route('/delete_editor', methods=['POST'])
@jwt_required()
def delete_editor():
    current_user_email = get_jwt_identity()
    data = request.get_json()
    return delete_editor(data['editor_id'], current_user_email)



@user_bp.route('/adm')
def adm():
    get_adm()



