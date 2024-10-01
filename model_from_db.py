import datetime
from typing import Any, List, Optional
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
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.mutable import MutableDict


class Base(DeclarativeBase):
    pass


class Users(Base):
    __tablename__ = "users"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="users_pkey"),
        Index("ix_users_email", "email", unique=True),
        Index("ix_users_id", "id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[Optional[str]] = mapped_column(String)
    password: Mapped[Optional[str]] = mapped_column(String)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean)
    is_superuser: Mapped[Optional[bool]] = mapped_column(Boolean)
    is_removable: Mapped[Optional[bool]] = mapped_column(Boolean)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime, server_default=text("now()")
    )
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime, server_default=text("now()")
    )
    deleted_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    profiles: Mapped[List["Profiles"]] = relationship("Profiles", back_populates="user")


class Profiles(Base):
    __tablename__ = "profiles"
    __table_args__ = (
        ForeignKeyConstraint(["user_id"], ["users.id"], name="profiles_user_id_fkey"),
        PrimaryKeyConstraint("id", name="profiles_pkey"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer)
    profile: Mapped[Optional[Any]] = mapped_column(MutableDict.as_mutable(HSTORE))

    user: Mapped["Users"] = relationship("Users", back_populates="profiles")
