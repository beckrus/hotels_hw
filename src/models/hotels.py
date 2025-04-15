from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, UniqueConstraint


class HotelsOrm(Base):
    __tablename__ = "hotels"
    __table_args__ = (
        UniqueConstraint('title', 'location', name='unique_hotel'),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), unique=True)
    location: Mapped[str]
