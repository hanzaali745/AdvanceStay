import enum
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, Enum, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.products.models import Product


class VerificationStatus(str, enum.Enum):
    UNVERIFIED = "unverified"
    PENDING = "pending"
    VERIFIED = "verified"


class Supplier(Base):
    """A sourcing supplier: identity, connector availability, and verification state."""

    __tablename__ = "suppliers"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    website: Mapped[str | None] = mapped_column(String(500))
    country: Mapped[str | None] = mapped_column(String(100))
    category: Mapped[str | None] = mapped_column(String(255))

    api_available: Mapped[bool] = mapped_column(Boolean, default=False)
    csv_available: Mapped[bool] = mapped_column(Boolean, default=False)
    xml_available: Mapped[bool] = mapped_column(Boolean, default=False)
    affiliate_feed: Mapped[bool] = mapped_column(Boolean, default=False)
    manual_import: Mapped[bool] = mapped_column(Boolean, default=True)

    minimum_order: Mapped[str | None] = mapped_column(String(100))
    shipping_notes: Mapped[str | None] = mapped_column(Text)
    marketplace_permissions: Mapped[str | None] = mapped_column(Text)

    verification_status: Mapped[VerificationStatus] = mapped_column(
        Enum(VerificationStatus), default=VerificationStatus.UNVERIFIED, nullable=False
    )
    last_checked: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    products: Mapped[list["Product"]] = relationship(back_populates="supplier")
