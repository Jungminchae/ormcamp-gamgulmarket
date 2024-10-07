import datetime
from typing import Any, List, Optional, TYPE_CHECKING
from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKeyConstraint,
    Index,
    Integer,
    PrimaryKeyConstraint,
    String,
    text,
)
from sqlalchemy.dialects.postgresql import HSTORE
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.mutable import MutableDict
from app.models.base import Base

if TYPE_CHECKING:
    from app.models.products import Product


# sqlacodegen으로 생성
class User(Base):
    """
    이 미니 프로젝트에서는 user가 회원가입할 때 email과 password만 입력한다고 가정
    가입의 다른 프로세스는 생략함
    """

    __tablename__ = "users"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="users_pkey"),
        Index("ix_users_email", "email", unique=True),
        Index("ix_users_id", "id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[Optional[str]] = mapped_column(String)
    password: Mapped[Optional[str]] = mapped_column(String)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, default=True)
    is_superuser: Mapped[Optional[bool]] = mapped_column(Boolean, default=False)
    is_removable: Mapped[Optional[bool]] = mapped_column(Boolean, default=False)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text("now()"))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text("now()"))
    deleted_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    resignation_reason: Mapped[Optional[str]] = mapped_column(String(255))

    profiles: Mapped[List["Profile"]] = relationship("Profile", back_populates="users")
    products: Mapped[List["Product"]] = relationship("Product", back_populates="user")


class Profile(Base):
    __tablename__ = "profiles"
    __table_args__ = (
        ForeignKeyConstraint(["user_id"], ["users.id"], name="profiles_user_id_fkey", ondelete="CASCADE"),
        PrimaryKeyConstraint("id", name="profiles_pkey"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=True)
    profile: Mapped[Optional[Any]] = mapped_column(MutableDict.as_mutable(HSTORE))

    users: Mapped["User"] = relationship("User", back_populates="profiles")
