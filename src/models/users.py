from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean


class UsersOrm(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(200), unique=True)
    first_name: Mapped[str] = mapped_column(String(200), nullable=True)
    last_name: Mapped[str] = mapped_column(String(200), nullable=True)
    email: Mapped[str] = mapped_column(String(200), nullable=True, unique=True)
    phone: Mapped[str] = mapped_column(String(200), nullable=True, unique=True)
    password_hash: Mapped[str] = mapped_column(String(200))
    is_varified: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
