import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from typing import Optional
from datetime import datetime, timezone
from sqlalchemy.orm import Mapped, mapped_column
from ..db import db

class User(db.Model, UserMixin):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(db.String(50), unique=True)
    role: Mapped[str] = mapped_column(db.String(20))
    name: Mapped[str] = mapped_column(db.String(20))
    surname: Mapped[str] = mapped_column(db.String(20))
    thirdname: Mapped[str] = mapped_column(db.String(20))
    phone: Mapped[str] = mapped_column(db.String(20))
    telegram_id: Mapped[str] = mapped_column(db.String(50))
    image: Mapped[str] = mapped_column(db.String(100), default=None, nullable=True)
    is_approved: Mapped[bool] = mapped_column(db.Boolean)

    password_salt: Mapped[str] = mapped_column(db.String(32), nullable=False)
    password_hash: Mapped[str] = mapped_column(db.String(256), nullable=False)

    created_at: Mapped[datetime] = mapped_column(db.DateTime,
                                                 index=True, default=lambda: datetime.now())
    deleted_at: Mapped[Optional[datetime]] = mapped_column(db.DateTime, nullable=True)

    def soft_delete(self):
        self.deleted_at = datetime.now()

    def set_password(self, password):
        self.password_salt = os.urandom(16).hex()
        salted_password = password + self.password_salt
        self.password_hash = generate_password_hash(salted_password)

    def check_password(self, password):
        salted_password = password + self.password_salt
        return check_password_hash(self.password_hash, salted_password)
