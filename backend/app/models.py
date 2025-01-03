import secrets
import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional

import sqlalchemy as sa
import sqlalchemy.orm as so
from werkzeug.security import check_password_hash, generate_password_hash

from app import db


class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = db.paginate(query, page=page, per_page=per_page, error_out=False)
        data = {
            "items": [item.to_dict() for item in resources.items],
        }
        return data


class User(PaginatedAPIMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    token: so.Mapped[Optional[str]] = so.mapped_column(
        sa.String(32), index=True, unique=True
    )
    token_expiration: so.Mapped[Optional[datetime]]

    def __repr__(self):
        return "<User {}>".format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self, include_email=False):
        data = {
            "id": self.id,
            "username": self.username,
        }
        if include_email:
            data["email"] = self.email
        return data

    def from_dict(self, data, new_user=False):
        for field in ["username", "email"]:
            if field in data:
                setattr(self, field, data[field])
        if new_user and "password" in data:
            self.set_password(data["password"])

    def get_token(self, expires_in=3600):
        now = datetime.now(timezone.utc)
        if self.token and self.token_expiration.replace(
            tzinfo=timezone.utc
        ) > now + timedelta(seconds=60):
            return self.token
        self.token = secrets.token_hex(16)
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.now(timezone.utc) - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        user = db.session.scalar(sa.select(User).where(User.token == token))
        if user is None or user.token_expiration.replace(
            tzinfo=timezone.utc
        ) < datetime.now(timezone.utc):
            return None
        return user


class Event(PaginatedAPIMixin, db.Model):
    id: so.Mapped[uuid.UUID] = so.mapped_column(
        sa.UUID, primary_key=True, default=uuid.uuid4
    )
    title: so.Mapped[str] = so.mapped_column(sa.String(64))
    start: so.Mapped[datetime] = so.mapped_column(sa.DateTime)

    def to_dict(self):
        data = {
            "id": self.id,
            "title": self.title,
            "start": self.to_jasmine_datetime(self.start),
        }
        return data

    def from_dict(self, data):
        for field in ["title"]:
            if field in data:
                setattr(self, field, data[field])
        for field in ["start"]:
            if field in data:
                setattr(self, field, self.from_jasmine_datetime(data[field]))

    @staticmethod
    def from_jasmine_datetime(datetime_str: str) -> datetime:
        return datetime.fromisoformat(datetime_str)
    
    @staticmethod
    def to_jasmine_datetime(datetime_obj: datetime) -> str:
        return datetime_obj.isoformat()
