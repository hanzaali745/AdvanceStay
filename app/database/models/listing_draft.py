from sqlalchemy import Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.session import Base
from app.database.models.mixins import TimestampMixin


class ListingDraft(Base, TimestampMixin):
    """
    Output of the Listing Agent. A draft only — never published
    automatically (see CLAUDE.md "Listing Agent: Do not publish
    automatically").
    """

    __tablename__ = "listing_drafts"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False, index=True)
    product: Mapped["Product"] = relationship()

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    item_specifics: Mapped[str | None] = mapped_column(Text, comment="Newline-separated key: value pairs")
    keywords: Mapped[str | None] = mapped_column(String(1000), comment="Comma-separated keywords")
    suggested_price: Mapped[float | None] = mapped_column(Float)

    def __repr__(self) -> str:  # pragma: no cover
        return f"<ListingDraft id={self.id} product_id={self.product_id} title={self.title!r}>"
