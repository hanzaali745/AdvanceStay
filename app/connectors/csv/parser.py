"""
CSV supplier-feed parser. Turns raw CSV rows into SupplierImportRow
objects the Supplier Agent can persist. Column names are matched
case-insensitively against a small set of common aliases per field —
add aliases here as real supplier feeds are onboarded, rather than
guessing at a supplier's schema.

A row with no recognisable "name" column is skipped and reported back
in `errors` rather than silently dropped or invented.
"""
import csv
from dataclasses import dataclass
from io import StringIO

from app.agents.supplier_agent import SupplierImportRow
from app.connectors.shared import FIELD_ALIASES, parse_float, parse_int


@dataclass
class CsvParseResult:
    rows: list[SupplierImportRow]
    errors: list[str]


def _build_header_map(fieldnames: list[str]) -> dict[str, str]:
    lowered = {fn.strip().lower(): fn for fn in fieldnames}
    header_map: dict[str, str] = {}
    for field, aliases in FIELD_ALIASES.items():
        for alias in aliases:
            if alias in lowered:
                header_map[field] = lowered[alias]
                break
    return header_map


def parse_csv(content: str) -> CsvParseResult:
    reader = csv.DictReader(StringIO(content))
    if not reader.fieldnames:
        return CsvParseResult(rows=[], errors=["CSV has no header row"])

    header_map = _build_header_map(reader.fieldnames)
    if "name" not in header_map:
        return CsvParseResult(rows=[], errors=["Could not find a product name column in the CSV header"])

    rows: list[SupplierImportRow] = []
    errors: list[str] = []

    for i, raw_row in enumerate(reader, start=2):  # header is line 1
        name = (raw_row.get(header_map["name"]) or "").strip()
        if not name:
            errors.append(f"Row {i}: missing product name — skipped")
            continue

        rows.append(
            SupplierImportRow(
                name=name,
                brand=(raw_row.get(header_map.get("brand", "")) or "").strip() or None,
                ean=(raw_row.get(header_map.get("ean", "")) or "").strip() or None,
                sku=(raw_row.get(header_map.get("sku", "")) or "").strip() or None,
                buy_price=parse_float(raw_row.get(header_map.get("buy_price", ""))),
                stock=parse_int(raw_row.get(header_map.get("stock", ""))),
                weight_kg=parse_float(raw_row.get(header_map.get("weight_kg", ""))),
                image_url=(raw_row.get(header_map.get("image_url", "")) or "").strip() or None,
                supplier_link=(raw_row.get(header_map.get("supplier_link", "")) or "").strip() or None,
            )
        )

    return CsvParseResult(rows=rows, errors=errors)
