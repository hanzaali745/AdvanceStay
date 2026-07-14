from datetime import datetime, timezone

from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.session import Base


class AgentRun(Base):
    """
    Audit log of every agent execution. Agents never call each other
    directly — this table (plus the product/supplier tables they read
    and write) is how the pipeline coordinates and how failures/decisions
    stay inspectable after the fact.
    """

    __tablename__ = "agent_runs"

    id: Mapped[int] = mapped_column(primary_key=True)

    agent_name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(20), default="success")  # success | failed | skipped
    items_processed: Mapped[int] = mapped_column(default=0)
    summary: Mapped[str | None] = mapped_column(Text)
    error: Mapped[str | None] = mapped_column(Text)

    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    def __repr__(self) -> str:  # pragma: no cover
        return f"<AgentRun id={self.id} agent={self.agent_name!r} status={self.status}>"
