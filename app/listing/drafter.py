"""
Pure listing-draft generation from data already on the product row. No
external calls — this is templated text generation, not AI copywriting,
so it never invents specifics the supplier/marketplace data didn't
provide.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class ListingContent:
    title: str
    description: str
    item_specifics: str
    keywords: str
    suggested_price: float | None


def draft_listing(
    *,
    name: str,
    brand: str | None,
    ean: str | None,
    sku: str | None,
    estimated_sell_price: float | None,
) -> ListingContent:
    title_parts = [p for p in (brand, name) if p]
    title = " ".join(title_parts)[:80]

    specifics_lines = []
    if brand:
        specifics_lines.append(f"Brand: {brand}")
    if ean:
        specifics_lines.append(f"EAN: {ean}")
    if sku:
        specifics_lines.append(f"MPN/SKU: {sku}")
    item_specifics = "\n".join(specifics_lines) or "No item specifics available yet"

    description_lines = [
        f"{title}",
        "",
        "Brand new, genuine item sourced from an authorised supplier." if brand else "Brand new item.",
    ]
    if ean:
        description_lines.append(f"EAN: {ean}")
    description = "\n".join(description_lines)

    keyword_pool = [w for w in (brand, name) if w]
    keywords = ", ".join(dict.fromkeys(" ".join(keyword_pool).split()))

    return ListingContent(
        title=title or name,
        description=description,
        item_specifics=item_specifics,
        keywords=keywords,
        suggested_price=estimated_sell_price,
    )
