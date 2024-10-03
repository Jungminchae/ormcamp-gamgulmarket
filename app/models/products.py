import datetime
from typing import Optional, TYPE_CHECKING
from sqlalchemy import DateTime, ForeignKeyConstraint, Integer, PrimaryKeyConstraint, String, Text, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base

if TYPE_CHECKING:
    from app.models.users import User


class Product(Base):
    __tablename__ = "products"
    __table_args__ = (
        ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE", name="products_user_id_fkey"),
        PrimaryKeyConstraint("id", name="products_pkey"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    price: Mapped[int] = mapped_column(Integer)
    user_id: Mapped[int] = mapped_column(Integer)
    description: Mapped[Optional[str]] = mapped_column(Text)
    image: Mapped[Optional[str]] = mapped_column(String(255))
    citrus_variety: Mapped[Optional[str]] = mapped_column(String(255))
    cultivation_region: Mapped[Optional[str]] = mapped_column(String(50))
    harvest_time: Mapped[Optional[str]] = mapped_column(String(50))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text("now()"))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text("now()"))

    user: Mapped["User"] = relationship("User", back_populates="products")
