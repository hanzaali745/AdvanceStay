from datetime import datetime

from sqlalchemy import Boolean, DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.session import Base
from app.database.models.mixins import TimestampMixin


class Supplier(Base, TimestampMixin):
    __tablename__ = "suppliers"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    website: Mapped[str | None] = mapped_column(String(500))
    country: Mapped[str | None] = mapped_column(String(100))
    category: Mapped[str | None] = mapped_column(String(255))

    # Availability of import methods — used by connectors to decide how to import
    api_available: Mapped[bool] = mapped_column(Boolean, default=False)
    csv_available: Mapped[bool] = mapped_column(Boolean, default=False)
    xml_available: Mapped[bool] = mapped_column(Boolean, default=False)
    affiliate_feed: Mapped[bool] = mapped_column(Boolean, default=False)
    manual_import: Mapped[bool] = mapped_column(Boolean, default=True)

    minimum_order: Mapped[str | None] = mapped_column(String(255))
    shipping_notes: Mapped[str | None] = mapped_column(Text)
    marketplace_permissions: Mapped[str | None] = mapped_column(
        Text, comment="Free-text notes on which marketplaces this supplier authorises resale on"
    )

    verification_status: Mapped[str] = mapped_column(String(50), default="unverified")
    last_checked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    products: Mapped[list["Product"]] = relationship(back_populates="supplier", cascade="all, delete-orphan")

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Supplier id={self.id} name={self.name!r}>"
