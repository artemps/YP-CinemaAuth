import uuid
from typing import Set

from sqlalchemy import ForeignKey, Enum, Column, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column

from core.database import Base, metadata
from repository.schemas import Roles


association_table = Table(
    "users_roles_map",
    metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("role_name",  ForeignKey("users_roles.name"), primary_key=True)
)


class UserRole(Base):
    __tablename__ = "users_roles"
    metadata = metadata

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[Roles] = mapped_column(Enum(Roles), unique=True, nullable=False)

    users: Mapped[Set["User"]] = relationship(
        "User", back_populates="roles", secondary=association_table, collection_class=set
    )

    def __repr__(self) -> str:
        return f"<UserRole {self.name}>"

    def __str__(self) -> str:
        return f"{self.name}"

