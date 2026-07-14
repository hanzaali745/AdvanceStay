"""
Base class and shared contract for all sourcing-pipeline agents.

Rules (see CLAUDE.md "AI Agents"):
- Agents read their input exclusively from the database.
- Agents write their output exclusively to the database.
- Agents never import or call another agent directly — coordination
  happens only by one agent's DB writes becoming the next agent's DB
  reads (typically orchestrated by app.agents.orchestrator).
- Every run is logged to `agent_runs` so status/failures are inspectable
  from the dashboard without reading logs.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.database.models import AgentRun


@dataclass
class AgentResult:
    items_processed: int = 0
    summary: str = ""


class BaseAgent(ABC):
    name: str = "base_agent"

    def __init__(self, db: Session):
        self.db = db

    @abstractmethod
    def run(self) -> AgentResult:
        """Perform the agent's work. Must only touch the database."""
        raise NotImplementedError

    def execute(self) -> AgentRun:
        """Runs the agent and records the outcome in agent_runs."""
        agent_run = AgentRun(agent_name=self.name, status="running", started_at=datetime.now(timezone.utc))
        self.db.add(agent_run)
        self.db.commit()
        self.db.refresh(agent_run)

        try:
            result = self.run()
            agent_run.status = "success"
            agent_run.items_processed = result.items_processed
            agent_run.summary = result.summary
        except NotImplementedError as exc:
            agent_run.status = "skipped"
            agent_run.summary = str(exc)
        except Exception as exc:  # noqa: BLE001 — must always persist the failure to the DB
            agent_run.status = "failed"
            agent_run.error = str(exc)
            self.db.rollback()
        finally:
            agent_run.finished_at = datetime.now(timezone.utc)
            self.db.add(agent_run)
            self.db.commit()

        return agent_run
