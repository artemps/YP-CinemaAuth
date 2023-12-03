import datetime as dt
import uuid

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column

from core.database import Base, metadata


class UserLogin(Base):
    __tablename__ = "users_logins"
    metadata = metadata

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    login_at: Mapped[dt.datetime] = mapped_column(DateTime, insert_default=func.now(), nullable=False)
    ip_address: Mapped[str] = mapped_column(String(50), nullable=False)
    user_agent: Mapped[str] = mapped_column(String(255), nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="last_logins")

    def __repr__(self) -> str:
        return f"<UserLogin {self.user_id} - {self.login_at}>"

    def __str__(self) -> str:
        return f"{self.user_id} - {self.login_at}"
