import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from core.database import Base, metadata


class User(Base):
    __tablename__ = "users"
    metadata = metadata

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    login = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # last_logins = relationship("UserLogins", foreign_keys="users_logins.id")
    # roles = relationship("Role", secondary="users_roles", back_populates="users")

    def __repr__(self) -> str:
        return f"<User {self.login}>"


class UserLogin(Base):
    __tablename__ = "users_logins"
    metadata = metadata

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey(User.id), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

#
# class Role(Base):
#     __tablename__ = "roles"
#     metadata = metadata
#
#     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
#     created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
#
#     users = relationship("User", secondary="users_roles", back_populates="roles")
#
#
# class UserRole(Base):
#     __tablename__ = "users_roles"
#     metadata = metadata
#
#     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
#     user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
#     role_id = Column(UUID(as_uuid=True), ForeignKey("roles.id"), nullable=False)
