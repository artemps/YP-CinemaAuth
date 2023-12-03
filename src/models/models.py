import uuid
from datetime import datetime
from typing import List

from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped

from core.database import Base, metadata


class User(Base):
    __tablename__ = "users"
    metadata = metadata

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    last_logins: Mapped[List["UserLogin"]] = relationship()

    def __repr__(self) -> str:
        return f"<User {self.email}>"


class UserLogin(Base):
    __tablename__ = "users_logins"
    metadata = metadata

    id: Mapped[int] = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey(User.id), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

