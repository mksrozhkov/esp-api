# stdlib
from datetime import datetime

# thirdparty
from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Measurement(Base):
    __tablename__ = "measurement"

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    temp: Mapped[int]
    humidity: Mapped[int]
    pressure: Mapped[int]
