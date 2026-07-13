import enum
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import JSON, DateTime, Enum, Float, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.suppliers.models import Supplier


class DataSource(str, enum.Enum):
    """Provenance tag for any individual product field. Never silently treat a value as
    verified when it is only imported, estimated, or absent."""

    VERIFIED = "verified"
    IMPORTED = "imported"
    ESTIMATED = "estimated"
    MISSING = "missing"


class Verdict(str, enum.Enum):
    BUY_NOW = "buy_now"
    TEST_BUY = "test_buy"
    WATCH = "watch"
    SKIP = "skip"


class Product(Base):
    """A candidate resale product with sourcing economics, agent scores, and a verdict.

    `data_sources` maps a field name (e.g. "buy_price", "demand") to a DataSource value,
    so the UI can always show the user where a number came from instead of implying
    every figure is equally verified.
    """

    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    supplier_id: Mapped[int] = mapped_column(ForeignKey("suppliers.id"), nullable=False)

    name: Mapped[str] = mapped_column(String(500), nullable=False)
    brand: Mapped[str | None] = mapped_column(String(255))
    ean: Mapped[str | None] = mapped_column(String(50), index=True)
    sku: Mapped[str | None] = mapped_column(String(100), index=True)
    supplier_link: Mapped[str | None] = mapped_column(String(1000))
    image_url: Mapped[str | None] = mapped_column(String(1000))

    buy_price: Mapped[float | None] = mapped_column(Float)
    estimated_sell_price: Mapped[float | None] = mapped_column(Float)
    fees: Mapped[float | None] = mapped_column(Float)
    shipping_cost: Mapped[float | None] = mapped_column(Float)
    packaging_cost: Mapped[float | None] = mapped_column(Float)
    returns_allowance: Mapped[float | None] = mapped_column(Float)

    profit: Mapped[float | None] = mapped_column(Float)
    roi: Mapped[float | None] = mapped_column(Float)
    break_even: Mapped[float | None] = mapped_column(Float)

    competition: Mapped[float | None] = mapped_column(Float)
    demand: Mapped[float | None] = mapped_column(Float)
    weight: Mapped[float | None] = mapped_column(Float)

    trend_score: Mapped[float | None] = mapped_column(Float)
    risk_score: Mapped[float | None] = mapped_column(Float)
    confidence_score: Mapped[float | None] = mapped_column(Float)

    verdict: Mapped[Verdict | None] = mapped_column(Enum(Verdict))
    verdict_reason: Mapped[str | None] = mapped_column(Text)
    watchlist: Mapped[bool] = mapped_column(default=False)

    data_sources: Mapped[dict] = mapped_column(JSON, default=dict)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    supplier: Mapped["Supplier"] = relationship(back_populates="products")
    price_history: Mapped[list["PriceHistory"]] = relationship(
        back_populates="product", cascade="all, delete-orphan"
    )


class PriceHistory(Base):
    """A single observed supplier price point, feeding the Price Drop Agent."""

    __tablename__ = "price_history"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    source: Mapped[DataSource] = mapped_column(Enum(DataSource), default=DataSource.IMPORTED, nullable=False)
    recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    product: Mapped["Product"] = relationship(back_populates="price_history")
