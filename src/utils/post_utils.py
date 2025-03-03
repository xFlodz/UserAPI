import os
import base64
from flask import current_app
from sqlalchemy import func
from transliterate import translit


def generate_post_address(header):
    address = translit(header, reversed=True).lower().replace(' ', '_')
    return address


def get_next_filename(folder, extension):
    if not os.path.exists(folder):
        os.makedirs(folder)
        return f'1.{extension}'

    existing_files = [f for f in os.listdir(folder) if f.endswith(f".{extension}")]
    numbers = []

    for file in existing_files:
        try:
            num = int(file.split('.')[0])
            numbers.append(num)
        except ValueError:
            continue

    next_number = max(numbers, default=0) + 1
    return f'{next_number}.{extension}'

def save_image(image, post_address, image_type):
    image_folder = f'src/assets/{post_address}/{image_type}'
    os.makedirs(image_folder, exist_ok=True)

    if isinstance(image, str) and image.startswith('data:image'):
        image_format = image.split(";")[0].split("/")[1]
        base64_data = image.split(",")[1]
        image_data = base64.b64decode(base64_data)

        filename = get_next_filename(image_folder, image_format)
        image_path = os.path.join(image_folder, filename)

        if not allowed_file(filename):
            raise Exception(f'Недопустимое расширение файла: {filename}')

        with open(image_path, 'wb') as f:
            f.write(image_data)

        return image_path


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_IMAGE_EXTENSIONS']


def convert_json_date_to_sqlite_format(json_date, date_key):
    return func.date(
        func.substr(func.json_extract(json_date, date_key), 7, 4) + '-' +
        func.substr(func.json_extract(json_date, date_key), 4, 2) + '-' +
        func.substr(func.json_extract(json_date, date_key), 1, 2)
    )