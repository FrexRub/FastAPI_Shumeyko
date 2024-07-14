from sqlalchemy import DateTime, Column, Integer, String, Table
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Operation(Base):
    __nametable__ = "operation"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    quantity: Mapped[str]
    figi: Mapped[str]
    instrument_type: Mapped[str] = mapped_column(nullable=True)
    date: Mapped[DateTime]
    type: Mapped[str]
