import datetime as dt
import uuid
from typing import List, Set

from sqlalchemy import DateTime, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column

from core.database import Base, metadata
from .user_roles import association_table as user_role_association_table


class User(Base):
    __tablename__ = "users"
    metadata = metadata

    # fields
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    login: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False, default="")
    last_name: Mapped[str] = mapped_column(String(50), nullable=False, default="")
    created_at: Mapped[dt.datetime] = mapped_column(DateTime, insert_default=func.now(), nullable=False)

    # relationship
    last_logins: Mapped[List["UserLogin"]] = relationship(
        "UserLogin", back_populates="user", order_by="desc(UserLogin.login_at)", cascade="all, delete"
    )
    roles: Mapped[Set["UserRole"]] = relationship(
        "UserRole", secondary=user_role_association_table, collection_class=set, back_populates="users", lazy="joined"
    )

    def __repr__(self) -> str:
        return f"<User {self.login}>"

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
