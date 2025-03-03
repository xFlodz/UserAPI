import random
import string

def generate_password(length=12):
    if length < 6:
        raise ValueError('Длина пароля должна быть не менее 6 символов')

    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))

    return password
