import random
import string
import base64
import os
from PIL import Image
from io import BytesIO

def generate_password(length=12):
    if length < 6:
        raise ValueError('Длина пароля должна быть не менее 6 символов')

    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))

    return password


def process_and_save_profile_image(file_storage, user_id):
    try:
        image = Image.open(file_storage)

        image.thumbnail((1024, 1024))

        user_dir = os.path.join("src", "assets", str(user_id))
        os.makedirs(user_dir, exist_ok=True)

        image_path = os.path.join(user_dir, "profile_image.jpeg")

        image.convert("RGB").save(image_path, format="JPEG", quality=85)

        return image_path
    except Exception as e:
        print("Ошибка обработки изображения:", e)
        return None