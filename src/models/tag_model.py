from ..db import db
from typing import Optional
from datetime import datetime, timezone
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Tag(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(50))

    tags_in_post = relationship('TagInPost', back_populates='tag', overlaps="posts_in_tag")

    created_at: Mapped[datetime] = mapped_column(db.DateTime, index=True, default=lambda: datetime.now())
    deleted_at: Mapped[Optional[datetime]] = mapped_column(db.DateTime, nullable=True)

    def soft_delete(self):
        self.deleted_at = datetime.now()
