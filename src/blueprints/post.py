from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.services.post_service import (
    create_post_service,
    delete_post_service,
    edit_post_service,
    get_all_posts_service,
    get_post_by_address_service
)

post_bp = Blueprint('post', __name__)

@post_bp.route('/create', methods=['POST'])
@jwt_required(refresh=True)
def create_post():
    data = request.json
    current_user_email = get_jwt_identity()

    try:
        post = create_post_service(data, current_user_email)
        return jsonify({'message': 'Пост создан успешно', 'post_id': post.id}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 400


@post_bp.route('/delete/<string:post_address>', methods=['DELETE'])
@jwt_required(refresh=True)
def delete_post(post_address):
    current_user_email = get_jwt_identity()

    try:
        delete_post_service(post_address, current_user_email)
        return jsonify({'message': 'Пост удален успешно'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400


@post_bp.route('/edit/<string:post_address>', methods=['PUT'])
@jwt_required(refresh=True)
def edit_post(post_address):
    data = request.json
    current_user_email = get_jwt_identity()

    try:
        updated_post = edit_post_service(post_address, data, current_user_email)
        return jsonify({'message': 'Пост обновлен успешно', 'post_id': updated_post.id}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400


@post_bp.route('/get_all_posts', methods=['GET', 'POST'])
def get_all_posts():
    try:
        filters = request.get_json()

        date_filter_type = filters.get('dateFilterType')
        tags_filter = filters.get('tagsFilter')
        start_date = filters.get('startDate')
        end_date = filters.get('endDate')


        posts = get_all_posts_service(date_filter_type, start_date, end_date, tags_filter)
        return jsonify(posts), 200

    except Exception as e:
        print(f"Ошибка на сервере: {str(e)}")
        return jsonify({'error': str(e)}), 500


@post_bp.route('/get_post/<string:post_address>', methods=['GET'])
def get_post_by_address(post_address):

    try:
        post = get_post_by_address_service(post_address)
        if post:
            return jsonify(post), 200
        return jsonify({'error': 'Пост не найден'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500
