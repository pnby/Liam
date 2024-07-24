from datetime import datetime
from typing import Optional, override

from sqlalchemy import String, DateTime, BigInteger, UniqueConstraint, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from bot import Base


class User(Base):
    __tablename__ = 'users'

    tg_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(), nullable=False)
    name: Mapped[str] = mapped_column(String, primary_key=True, nullable=False)
    premium: Mapped[bool] = mapped_column(Boolean, nullable=False)
    username: Mapped[Optional[str]] = mapped_column(String, unique=False, nullable=True)
    password: Mapped[Optional[str]] = mapped_column(String, unique=False, nullable=True)
    is_disabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    __table_args__ = (
        UniqueConstraint('tg_id'),
    )

    @override
    def __eq__(self, other):
        if not isinstance(other, User):
            return NotImplemented
        return (self.tg_id == other.tg_id and
                self.name == other.name and
                self.premium == other.premium and
                self.username == other.username and
                self.password == other.password and
                self.created_at == other.created_at and
                self.updated_at == other.updated_at)
