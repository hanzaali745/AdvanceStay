"""
XML supplier-feed parser. Supports the common "root > repeated item
element > flat fields" shape used by most supplier/affiliate XML feeds
(e.g. Google Shopping-style <item>/<product> feeds). Nested/vendor-specific
XML schemas are an INTEGRATION POINT: add a dedicated parser function per
supplier under this package once a real feed sample is available rather
than trying to guess an unfamiliar schema.
"""
from dataclasses import dataclass
from xml.etree import ElementTree

from app.agents.supplier_agent import SupplierImportRow
from app.connectors.shared import FIELD_ALIASES, parse_float, parse_int

_ITEM_TAG_CANDIDATES = ("item", "product", "entry", "row")


@dataclass
class XmlParseResult:
    rows: list[SupplierImportRow]
    errors: list[str]


def _local_tag(tag: str) -> str:
    return tag.split("}")[-1].lower() if "}" in tag else tag.lower()


def _find_item_elements(root: ElementTree.Element) -> list[ElementTree.Element]:
    for candidate in _ITEM_TAG_CANDIDATES:
        matches = [el for el in root.iter() if _local_tag(el.tag) == candidate]
        if matches:
            return matches
    return []


def _extract_field(element: ElementTree.Element, field: str) -> str | None:
    for alias in FIELD_ALIASES[field]:
        for child in element:
            if _local_tag(child.tag) == alias.replace(" ", "_") or _local_tag(child.tag) == alias:
                return (child.text or "").strip() or None
    return None


def parse_xml(content: str) -> XmlParseResult:
    try:
        root = ElementTree.fromstring(content)
    except ElementTree.ParseError as exc:
        return XmlParseResult(rows=[], errors=[f"Invalid XML: {exc}"])

    items = _find_item_elements(root)
    if not items:
        return XmlParseResult(
            rows=[], errors=[f"No recognisable item elements found (expected one of {_ITEM_TAG_CANDIDATES})"]
        )

    rows: list[SupplierImportRow] = []
    errors: list[str] = []

    for i, element in enumerate(items, start=1):
        name = _extract_field(element, "name")
        if not name:
            errors.append(f"Item {i}: missing product name — skipped")
            continue

        rows.append(
            SupplierImportRow(
                name=name,
                brand=_extract_field(element, "brand"),
                ean=_extract_field(element, "ean"),
                sku=_extract_field(element, "sku"),
                buy_price=parse_float(_extract_field(element, "buy_price")),
                stock=parse_int(_extract_field(element, "stock")),
                weight_kg=parse_float(_extract_field(element, "weight_kg")),
                image_url=_extract_field(element, "image_url"),
                supplier_link=_extract_field(element, "supplier_link"),
            )
        )

    return XmlParseResult(rows=rows, errors=errors)
