from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.session import Base
from app.database.models.mixins import TimestampMixin


class Setting(Base, TimestampMixin):
    """
    User-editable key/value overrides for business defaults (budget,
    minimum ROI, fees, notification preferences, etc.). Falls back to
    app.settings.config.Settings (environment variables) when a key has
    no row here. API credentials/secrets are never stored in this table —
    those stay in environment variables only.
    """

    __tablename__ = "settings"

    key: Mapped[str] = mapped_column(String(100), primary_key=True)
    value: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str | None] = mapped_column(String(500))

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Setting {self.key}={self.value!r}>"
