from datetime import datetime, timezone
from typing import Optional

import sqlalchemy as sa
import sqlalchemy.orm as so

from app import db


class User(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(32), index=True, unique=True)
    pfp_url: so.Mapped[str] = so.mapped_column(sa.String(48))
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    tasks: so.WriteOnlyMapped["Task"] = so.relationship(back_populates="assignee")

    def __repr__(self) -> str:
        return f"<User {self.name}>"


class Task(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    title: so.Mapped[str] = so.mapped_column(sa.String(40))
    description: so.Mapped[Optional[str]] = so.mapped_column(sa.String(140))
    due_date: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc)
    )
    helpers: so.Mapped[Optional[str]] = so.mapped_column(sa.String(20))
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    assignee: so.Mapped[User] = so.relationship(back_populates="tasks")

    def __repr__(self) -> str:
        return f"<Task {self.title}>"
