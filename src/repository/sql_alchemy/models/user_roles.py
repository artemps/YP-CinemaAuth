import uuid
from typing import Set

from sqlalchemy import ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column

from core.database import Base, metadata
from repository.schemas import Roles


class UserRole(Base):
    __tablename__ = "users_roles"
    metadata = metadata

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[Roles] = mapped_column(Enum(Roles), unique=True, nullable=False)

    users: Mapped[Set["User"]] = relationship(
        "User", back_populates="roles", secondary="users_roles_map", collection_class=set
    )

    def __repr__(self) -> str:
        return f"<UserRole {self.user_id} - {self.name}>"

    def __str__(self) -> str:
        return f"{self.user_id} - {self.name}"


class UserRoleMap(Base):
    __tablename__ = "users_roles_map"
    metadata = metadata

    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    role_name: Mapped[Roles] = mapped_column(Enum(Roles), ForeignKey("users_roles.name"), primary_key=True)
