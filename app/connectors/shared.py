"""
Field-name aliases and value parsing shared by the CSV and XML supplier
connectors. Add aliases here as real supplier feeds are onboarded.
"""

FIELD_ALIASES: dict[str, tuple[str, ...]] = {
    "name": ("name", "title", "product_name", "product name"),
    "brand": ("brand", "manufacturer"),
    "ean": ("ean", "barcode", "gtin", "upc"),
    "sku": ("sku", "mpn", "product_code", "product code", "item_id"),
    "buy_price": ("buy_price", "price", "cost", "wholesale_price", "trade_price"),
    "stock": ("stock", "quantity", "qty", "stock_level"),
    "weight_kg": ("weight_kg", "weight", "weight(kg)"),
    "image_url": ("image_url", "image", "image_link"),
    "supplier_link": ("supplier_link", "url", "product_url", "link"),
}


def parse_float(raw: str | None) -> float | None:
    if raw is None or raw.strip() == "":
        return None
    try:
        return float(raw.replace(",", "").replace("£", "").replace("$", "").strip())
    except ValueError:
        return None


def parse_int(raw: str | None) -> int | None:
    value = parse_float(raw)
    return int(value) if value is not None else None
