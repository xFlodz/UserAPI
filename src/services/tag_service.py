from flask import jsonify
from src.db import db
from src.models import Tag, TagInPost, User
from datetime import datetime


def create_tag_service(data, current_user_email):
    try:
        name = data.get('name')

        user_current = User.query.filter_by(email=current_user_email).first()
        if user_current.role != 'admin':
            return jsonify({'error': 'У вас недостаточно прав'}), 403

        if not name:
            return jsonify({'error': 'Название тега обязательно'}), 400

        existing_tag = Tag.query.filter(Tag.name == name, Tag.deleted_at.is_(None)).first()
        if existing_tag:
            return jsonify({'error': 'Тег с таким названием уже существует'}), 400

        new_tag = Tag(name=name)
        db.session.add(new_tag)
        db.session.commit()

        return jsonify({
            'id': new_tag.id,
            'name': new_tag.name,
            'created_at': new_tag.created_at
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


def delete_tag_service(tag_id, current_user_email):
    try:
        tag = Tag.query.filter(Tag.id == tag_id, Tag.deleted_at.is_(None)).first()

        user_current = User.query.filter_by(email=current_user_email).first()
        if user_current.role != 'admin':
            return jsonify({'error': 'У вас недостаточно прав'}), 403

        if not tag:
            return jsonify({'error': 'Тег не найден'}), 404

        TagInPost.query.filter(TagInPost.tag_id == tag.id).delete()

        db.session.delete(tag)
        db.session.commit()

        return jsonify({'message': 'Тег удален успешно'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


def get_all_tags_service():
    try:
        tags = Tag.query.filter(Tag.deleted_at.is_(None)).all()
        tags_list = [{
            'id': tag.id,
            'name': tag.name,
            'created_at': tag.created_at
        } for tag in tags]

        return jsonify(tags_list), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
