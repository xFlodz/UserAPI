from src.db import db
from typing import Optional
from datetime import datetime, timezone
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

class TagInPost(db.Model):
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id', ondelete='CASCADE'), primary_key=True)
    tag_id: Mapped[int] = mapped_column(ForeignKey('tag.id', ondelete='CASCADE'), primary_key=True)

    post: Mapped['Post'] = relationship('Post', back_populates='tags_in_post', overlaps="tags_in_post")
    tag: Mapped['Tag'] = relationship('Tag', back_populates='tags_in_post', overlaps="posts_in_tag")

    created_at: Mapped[datetime] = mapped_column(db.DateTime, index=True, default=lambda: datetime.now())
    deleted_at: Mapped[Optional[datetime]] = mapped_column(db.DateTime, nullable=True)

    def soft_delete(self):
        self.deleted_at = datetime.now()
