import typing
from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

if typing.TYPE_CHECKING:
    from src.models import FacilitiesOrm


class RoomsOrm(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id", ondelete="CASCADE"))
    title: Mapped[str]
    description: Mapped[str | None]
    price: Mapped[int]
    quantity: Mapped[int]
    image_id: Mapped[str | None]

    facilities: Mapped[list["FacilitiesOrm"]] = relationship(
        back_populates="rooms", secondary="rooms_facilities", lazy="selectin"
    )
