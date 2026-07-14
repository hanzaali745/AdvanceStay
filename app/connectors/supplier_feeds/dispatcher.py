"""
Picks the right connector for a supplier's declared import method and
runs the Supplier Agent against the parsed rows. This is the single
entry point the suppliers router calls — it does not know about CSV/XML
parsing details itself.
"""
from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.agents.supplier_agent import SupplierAgent
from app.connectors.csv.parser import parse_csv
from app.connectors.xml.parser import parse_xml
from app.database.models import AgentRun


@dataclass
class ImportOutcome:
    agent_run: AgentRun
    parse_errors: list[str]


def import_supplier_file(
    db: Session, *, supplier_id: int, filename: str, content: str, full_catalog: bool = False
) -> ImportOutcome:
    lower_name = filename.lower()

    if lower_name.endswith(".csv"):
        result = parse_csv(content)
    elif lower_name.endswith(".xml"):
        xml_result = parse_xml(content)
        result = xml_result
    else:
        raise ValueError(f"Unsupported file type for '{filename}' — expected .csv or .xml")

    agent = SupplierAgent(db, supplier_id=supplier_id, rows=result.rows, full_catalog=full_catalog)
    agent_run = agent.execute()

    return ImportOutcome(agent_run=agent_run, parse_errors=result.errors)
