from sqlalchemy import ForeignKey, String, UniqueConstraint
from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column


class FacilitiesOrm(Base):
    __tablename__ = "facilities"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)


class RoomsFacilitiesOrm(Base):
    __tablename__ = "rooms_facilities"

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id", ondelete="CASCADE"))
    facility_id: Mapped[int] = mapped_column(
        ForeignKey("facilities.id", ondelete="CASCADE")
    )
    __table_args__ = (UniqueConstraint('room_id', 'facility_id', name='_rooms_facilities'),)