import os

import psycopg2
from datetime import datetime
from werkzeug.security import generate_password_hash

DB_HOST = "db"
DB_NAME = "user_db"
DB_USER = "postgres"
DB_PASSWORD = "q1w2e3"

conn = psycopg2.connect(
    host=DB_HOST,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)
cursor = conn.cursor()

password_salt = os.urandom(16).hex()
salted_password = '1234' + password_salt
password_hash = generate_password_hash(salted_password)

cursor.execute("SELECT id FROM \"user\" WHERE email = 'admin'")
if not cursor.fetchone():
    cursor.execute("""
        INSERT INTO "user" (
            email, role, name, surname, thirdname, phone, 
            telegram_id, is_approved, password_salt, password_hash, created_at
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
    """, (
        'admin', 'admin', 'Иван', 'Иван', 'Иван', '+79651111111',
        '@paveldurov', True, password_salt, password_hash,
        datetime.now()
    ))
    conn.commit()
    print("Администратор создан!")
else:
    print("Администратор уже существует")

cursor.close()
conn.close()