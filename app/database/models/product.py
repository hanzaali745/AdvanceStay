from sqlalchemy import Enum, Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.session import Base
from app.database.models.mixins import TimestampMixin
from app.database.models.enums import DataSource, Verdict


class Product(Base, TimestampMixin):
    """
    A candidate resale product, built up incrementally by the agent
    pipeline. Every value that can legitimately be unknown carries a
    matching `<field>_source` column so the UI never presents an estimate
    as verified fact.
    """

    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)

    # --- Identity ---
    name: Mapped[str] = mapped_column(String(500), nullable=False, index=True)
    brand: Mapped[str | None] = mapped_column(String(255))
    ean: Mapped[str | None] = mapped_column(String(50), index=True)
    sku: Mapped[str | None] = mapped_column(String(100), index=True)

    supplier_id: Mapped[int | None] = mapped_column(ForeignKey("suppliers.id"))
    supplier: Mapped["Supplier"] = relationship(back_populates="products")
    supplier_link: Mapped[str | None] = mapped_column(String(1000))
    image_url: Mapped[str | None] = mapped_column(String(1000))

    # --- Supplier-side data (Supplier Agent) ---
    buy_price: Mapped[float | None] = mapped_column(Float)
    buy_price_source: Mapped[DataSource] = mapped_column(Enum(DataSource), default=DataSource.MISSING)
    stock: Mapped[int | None] = mapped_column()
    stock_source: Mapped[DataSource] = mapped_column(Enum(DataSource), default=DataSource.MISSING)
    weight_kg: Mapped[float | None] = mapped_column(Float)
    is_discontinued: Mapped[bool] = mapped_column(default=False)

    # --- Bundle Agent output ---
    is_bundle: Mapped[bool] = mapped_column(default=False)
    bundle_quantity: Mapped[int | None] = mapped_column()

    # --- Marketplace data (Market Agent) ---
    estimated_sell_price: Mapped[float | None] = mapped_column(Float)
    sell_price_source: Mapped[DataSource] = mapped_column(Enum(DataSource), default=DataSource.MISSING)
    competition: Mapped[float | None] = mapped_column(Float, comment="0-100 relative competition score")
    competition_source: Mapped[DataSource] = mapped_column(Enum(DataSource), default=DataSource.MISSING)
    demand: Mapped[float | None] = mapped_column(Float, comment="0-100 relative demand score")
    demand_source: Mapped[DataSource] = mapped_column(Enum(DataSource), default=DataSource.MISSING)

    # --- Profit Agent output (always derived — never user/supplier supplied) ---
    marketplace_fees: Mapped[float | None] = mapped_column(Float)
    shipping_cost: Mapped[float | None] = mapped_column(Float)
    packaging_cost: Mapped[float | None] = mapped_column(Float)
    returns_allowance: Mapped[float | None] = mapped_column(Float)
    net_profit: Mapped[float | None] = mapped_column(Float)
    roi_percent: Mapped[float | None] = mapped_column(Float)
    break_even_units: Mapped[float | None] = mapped_column(Float)
    profit_margin_percent: Mapped[float | None] = mapped_column(Float)
    investment_required: Mapped[float | None] = mapped_column(Float)

    # --- Trend / Risk / Scoring Agent output ---
    trend_score: Mapped[float | None] = mapped_column(Float)
    risk_score: Mapped[float | None] = mapped_column(Float)
    risk_reasons: Mapped[str | None] = mapped_column(Text)
    confidence_score: Mapped[float | None] = mapped_column(Float)

    verdict: Mapped[Verdict | None] = mapped_column(Enum(Verdict))
    verdict_reason: Mapped[str | None] = mapped_column(Text)

    watchlist: Mapped[bool] = mapped_column(default=False)

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Product id={self.id} name={self.name!r} verdict={self.verdict}>"
