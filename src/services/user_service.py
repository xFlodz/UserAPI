from flask import jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity
from ..models.user_model import User
from .. import db
from ..utils.user_utils import generate_password


def register_user(data):
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Пользователь уже зарегистрирован'}), 409

    new_user = User(
        email=data['email'],
        role='user',
        name=data['name'],
        surname=data['surname']
    )
    new_user.set_password(data['password'])

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Пользователь успешно зарегистрирован'}), 201


def login_user(data):
    user = User.query.filter_by(email=data['login']).first()
    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Неверный логин или пароль'}), 401

    access_token = create_access_token(identity=user.email)
    refresh_token = create_refresh_token(identity=user.email)

    return jsonify(access_token=access_token, refresh_token=refresh_token, role=user.role, id=user.id), 200


def logout_user_service(current_user_email):
    user = User.query.filter_by(email=current_user_email).first()
    if not user:
        return jsonify({'error': 'Пользователь не найден'}), 404

    return jsonify({'message': 'Вы успешно вышли'}), 200


def add_editor_service(email, current_user_email):
    user_current = User.query.filter_by(email=current_user_email).first()
    if user_current.role != 'admin':
        return jsonify({'error': 'У вас недостаточно прав'}), 403

    user = User.query.filter_by(email=email).first()

    if not user:
        new_user = User(
            email=email,
            role='poster',
            name='Аноним',
            surname='Аноним'
        )

        password = generate_password()
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        print('Пользователь зарегестрирован', password)
        #Добавить отправку на почту
        return jsonify({'message': 'Зарегестрирован новый редактор'}), 200

    if user.role == 'poster':
        return jsonify({'message': 'Пользователь уже является редактором'}), 200

    user.role = 'poster'
    db.session.commit()

    return jsonify({'message': f'Пользователь {email} теперь редактор'}), 200


def get_all_editors(current_user_email):
    user_current = User.query.filter_by(email=current_user_email).first()
    if user_current.role != 'admin':
        return jsonify({'error': 'У вас недостаточно прав'}), 403

    editors = User.query.filter_by(role='poster').all()

    if not editors:
        return jsonify([]), 200

    editors_list = [
        {'id': editor.id, 'email': editor.email, 'name': editor.name, 'surname': editor.surname}
        for editor in editors
    ]

    return jsonify(editors_list), 200


def delete_editor_service(editor_email, current_user_email):
    user_current = User.query.filter_by(email=current_user_email).first()
    if user_current.role != 'admin':
        return jsonify({'error': 'У вас недостаточно прав'}), 403


    editor = User.query.filter_by(email=editor_email, role='poster').first()
    if not editor:
        return jsonify({'error': 'Редактор не найден'}), 404

    editor.role = 'user'
    db.session.commit()

    return jsonify({'message': f'Редактор с почтой {editor_email} успешно удален'}), 200


def get_user_by_id_service(id):
    user = User.query.filter_by(id=id).first()
    if user:
        user_data = {
            'id': user.id,
            'email': user.email,
            'name': user.name,
            'surname': user.surname,
            'role': user.role,
        }
        return user_data
    return jsonify({'message': 'Пользователь не найден'}), 404


def get_user_by_email_service(email):
    user = User.query.filter_by(email=email).first()
    if user:
        user_data = {
            'id': user.id,
            'email': user.email,
            'name': user.name,
            'surname': user.surname,
            'role': user.role,
        }
        return user_data
    return jsonify({'message': 'Пользователь не найден'}), 404


def change_password_service(data, current_user_email):
    user = User.query.filter_by(email=current_user_email).first()
    if not user:
        return jsonify({'error': 'У вас нет прав'}), 403

    old_password = data.get('old_password')
    new_password = data.get('new_password')

    if not user.check_password(old_password):
        return jsonify({'error': 'Старый пароль неверен'}), 400

    user.set_password(new_password)
    db.session.commit()

    return jsonify({'message': 'Пароль успешно изменен'}), 200


def update_profile_service(data, current_user_email):
    user = User.query.filter_by(email=current_user_email).first()
    if not user:
        return jsonify({'error': 'У вас нет прав'}), 403

    name = data.get('name')
    surname = data.get('surname')
    email = data.get('email')

    if email and email != user.email:
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Этот email уже занят'}), 400
        user.email = email

    if name:
        user.name = name
    if surname:
        user.surname = surname

    db.session.commit()

    updated_data = {
        'id': user.id,
        'email': user.email,
        'name': user.name,
        'surname': user.surname,
        'role': user.role
    }

    return jsonify({'message': 'Профиль обновлен', 'user': updated_data}), 200




def get_adm():
    user = User.query.filter_by(email='admin').first()
    if not user:
        user = User(email='admin', role='admin', name='Иван', surname='Иван')
        user2 = User(email='poster', role='poster', name='Иван', surname='Иван')
        user.set_password('1234')
        user2.set_password('1234')
        db.session.add(user)
        db.session.add(user2)
        db.session.commit()
        print('Успешно создан')
    else:
        print('Уже создан')
