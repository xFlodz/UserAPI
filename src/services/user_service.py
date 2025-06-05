from flask import jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity
from ..models.user_model import User
from .. import db
from ..utils.user_utils import generate_password, process_and_save_profile_image


def register_user(data):
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Пользователь уже зарегистрирован'}), 409

    new_user = User(
        email=data['email'],
        role='user',
        name=data.get('name'),
        surname=data.get('surname'),
        thirdname=data.get('thirdname'),
        phone=data.get('phone'),
        telegram_id=data.get('telegram_id'),
        is_approved=False
    )

    new_user.set_password(data['password'])

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Пользователь успешно зарегистрирован'}), 201


def login_user(data):
    user = User.query.filter_by(email=data['login']).first()
    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Неверный логин или пароль'}), 401
    if user.is_approved is False:
        return jsonify({'error': 'Ваш профиль еще не подтвержден'}), 401


    access_token = create_access_token(identity=user.email)
    refresh_token = create_refresh_token(identity=user.email)

    return jsonify(access_token=access_token, refresh_token=refresh_token, role=user.role, id=user.id), 200


def logout_user_service(current_user_email):
    user = User.query.filter_by(email=current_user_email).first()
    if not user:
        return jsonify({'error': 'Пользователь не найден'}), 404

    return jsonify({'message': 'Вы успешно вышли'}), 200


def change_role_service(data, current_user_email):
    user_current = User.query.filter_by(email=current_user_email).first()
    if user_current.role != 'admin':
        return jsonify({'error': 'У вас недостаточно прав'}), 403

    new_role = data.get('newRole')
    user_id = data.get('userId')

    user = User.query.filter_by(id=user_id).first()

    if not user:
        return jsonify({'message': 'Такого пользователя нет'}), 403

    user.role = new_role
    db.session.commit()

    return jsonify({'message': f'Роль пользователя изменена'}), 200


def get_all_editors():
    editors = User.query.filter(User.role.in_(['user', 'poster'])).order_by(User.surname).all()

    if not editors:
        return jsonify([]), 200

    editors_list = [
        {'id': editor.id,
         'name': editor.name,
         'surname': editor.surname,
         'thirdname': editor.thirdname,
         'role': editor.role,
         'image': editor.image,
         'is_approved': editor.is_approved}
        for editor in editors
    ]

    return jsonify(editors_list), 200

def approve_user_service(current_user_email, data):
    user_current = User.query.filter_by(email=current_user_email).first()
    if user_current.role != 'admin':
        return jsonify({'error': 'У вас недостаточно прав'}), 403

    user_id = data.get('user_id')
    user = User.query.filter_by(id=user_id).first()
    user.is_approved = True
    db.session.commit()

    return jsonify({'message': f'Пользователь успешно одобрен'}), 200

def delete_user_service(data, current_user_email):

    user_id = data.get('userId')

    user_current = User.query.filter_by(email=current_user_email).first()
    if user_current.role != 'admin':
        return jsonify({'error': 'У вас недостаточно прав'}), 403


    user = User.query.filter_by(id=user_id).first()
    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': f'Пользователь удален'}), 200


def get_user_by_id_service(id):
    user = User.query.filter_by(id=id).first()
    if user:
        user_data = {
            'id': user.id,
            'email': user.email,
            'name': user.name,
            'surname': user.surname,
            'role': user.role,
            'thirdname': user.thirdname,
            'telegram_id': user.telegram_id,
            'image': user.image,
            'phone': user.phone,
            'is_approved': user.is_approved
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
            'thirdname': user.thirdname,
            'telegram_id': user.telegram_id,
            'image': user.image,
            'phone': user.phone,
            'is_approved': user.is_approved
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


def update_profile_service(data, current_user_email, image):
    user = User.query.filter_by(email=current_user_email).first()
    if not user:
        return jsonify({'error': 'У вас нет прав'}), 403

    name = data.get('name')
    surname = data.get('surname')
    email = data.get('email')
    thirdname = data.get('thirdname')
    phone = data.get('phone')
    telegram_id = data.get('telegram_id')

    if email and email != user.email:
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Этот email уже занят'}), 400
        user.email = email

    if name:
        user.name = name
    if surname:
        user.surname = surname
    if thirdname:
        user.thirdname = thirdname
    if phone:
        user.phone = phone
    if telegram_id:
        user.telegram_id = telegram_id

    if image:
        print('image')
        image_path = process_and_save_profile_image(image, user.id)
        if image_path:
            user.image = image_path.replace("\\", "/")
        else:
            return jsonify({'error': 'Ошибка обработки изображения'}), 400

    db.session.commit()

    updated_data = {
        'id': user.id,
        'email': user.email,
        'name': user.name,
        'surname': user.surname,
        'role': user.role,
        'thirdname': user.thirdname,
        'telegram_id': user.telegram_id,
        'image': user.image,
        'phone': user.phone
    }

    return jsonify({'message': 'Профиль обновлен', 'user': updated_data}), 200




def get_adm():
    user = User.query.filter_by(email='admin').first()
    if not user:
        user = User(email='admin', role='admin', name='Иван', surname='Иван', thirdname='Иван', phone='+79651111111', telegram_id='@paveldurov', is_approved=True)
        user2 = User(email='poster', role='poster', name='Иван', surname='Иван', thirdname='Иван', phone='+79651111111', telegram_id='@paveldurov', is_approved=True)
        user.set_password('1234')
        user2.set_password('1234')
        db.session.add(user)
        db.session.add(user2)
        db.session.commit()
        print('Успешно создан')
    else:
        print('Уже создан')
