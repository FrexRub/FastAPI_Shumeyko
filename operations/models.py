import datetime

from sqlalchemy import DateTime, Integer, func
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Operation(Base):
    __tablename__ = "operations"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    quantity: Mapped[str]
    figi: Mapped[str]
    instrument_type: Mapped[str] = mapped_column(nullable=True)
    date: Mapped[DateTime] = mapped_column(
        DateTime,
        server_default=func.now(),
        default=datetime.datetime.utcnow(),
    )
    type: Mapped[str]
