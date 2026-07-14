"""Reads the latest AgentRun per agent for dashboard/status display."""
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.agents.orchestrator import PIPELINE_ORDER
from app.database.models import AgentRun

ALL_AGENT_NAMES = ["supplier_agent"] + [cls.name for cls in PIPELINE_ORDER]


def get_latest_agent_runs(db: Session) -> list[AgentRun]:
    subq = (
        select(AgentRun.agent_name, func.max(AgentRun.id).label("max_id"))
        .group_by(AgentRun.agent_name)
        .subquery()
    )
    stmt = select(AgentRun).join(subq, AgentRun.id == subq.c.max_id)
    latest_by_name = {run.agent_name: run for run in db.execute(stmt).scalars()}

    return [latest_by_name[name] for name in ALL_AGENT_NAMES if name in latest_by_name]
