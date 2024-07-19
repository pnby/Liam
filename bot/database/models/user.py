from datetime import datetime

from sqlalchemy import String, DateTime, BigInteger, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from bot import Base


class User(Base):
    __tablename__ = 'users'

    tg_id: Mapped[BigInteger] = mapped_column(BigInteger, primary_key=True, unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(), nullable=False)
    name: Mapped[String] = mapped_column(String, primary_key=True, nullable=False)
    username: Mapped[String] = mapped_column(String, unique=False, nullable=True)
    password: Mapped[String] = mapped_column(String, unique=False, nullable=True)

    __table_args__ = (
        UniqueConstraint('tg_id'),
    )
