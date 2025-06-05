from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..services.user_service import register_user, login_user, logout_user_service, get_adm, change_role_service, \
    get_all_editors, delete_user_service, get_user_by_id_service, get_user_by_email_service, update_profile_service, \
    change_password_service, approve_user_service

user_bp = Blueprint('user', __name__)


@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    return register_user(data)


@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    return login_user(data)

@user_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    current_user_email = get_jwt_identity()
    return logout_user_service(current_user_email)


@user_bp.route('/change_role', methods=['POST'])
@jwt_required(refresh=True)
def change_role():
    current_user_email = get_jwt_identity()
    data = request.get_json()

    return change_role_service(data, current_user_email)


@user_bp.route('/get_editors', methods=['GET'])
def get_editors():
    return get_all_editors()


@user_bp.route('/approve_user', methods=['POST'])
@jwt_required(refresh=True)
def approve_user():
    current_user_email = get_jwt_identity()
    data = request.get_json()
    return approve_user_service(current_user_email, data)


@user_bp.route('/delete_user', methods=['POST'])
@jwt_required(refresh=True)
def delete_user():
    current_user_email = get_jwt_identity()
    data = request.get_json()
    return delete_user_service(data, current_user_email)


@user_bp.route('get_user_by_id/<id>', methods=['GET'])
def get_user_by_id(id):
    return get_user_by_id_service(id)


@user_bp.route('get_user_by_email/<email>', methods=['GET'])
def get_user_by_email(email):
    return get_user_by_email_service(email)


@user_bp.route('/change_password', methods=['POST'])
@jwt_required()
def change_password():
    current_user_email = get_jwt_identity()
    data = request.get_json()
    return change_password_service(data, current_user_email)


@user_bp.route('/update_profile', methods=['POST'])
@jwt_required()
def update_profile():
    current_user_email = get_jwt_identity()
    data = request.form
    image_file = request.files.get('image')
    return update_profile_service(data, current_user_email, image_file)


@user_bp.route('/adm')
def adm():
    get_adm()



