from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.session import Base


class PriceHistory(Base):
    """
    One row per observed supplier buy_price for a product. Populated by
    the Supplier Agent on every import so the Price Drop Agent can detect
    falls without guessing at data it doesn't have.
    """

    __tablename__ = "price_history"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False, index=True)
    product: Mapped["Product"] = relationship()

    buy_price: Mapped[float] = mapped_column(Float, nullable=False)
    recorded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )

    def __repr__(self) -> str:  # pragma: no cover
        return f"<PriceHistory product_id={self.product_id} buy_price={self.buy_price}>"
