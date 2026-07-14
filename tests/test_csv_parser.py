from app.connectors.csv.parser import parse_csv


def test_parses_recognised_columns_with_aliases():
    content = "Name,Brand,EAN,SKU,Price,Qty,Weight(kg)\nWidget A,ACME,111,SKU-A,10.50,20,1.1\n"
    result = parse_csv(content)
    assert len(result.rows) == 1
    row = result.rows[0]
    assert row.name == "Widget A"
    assert row.buy_price == 10.5
    assert row.stock == 20
    assert result.errors == []


def test_skips_row_with_missing_name_and_reports_error():
    content = "Name,Price\n,10.00\n"
    result = parse_csv(content)
    assert result.rows == []
    assert len(result.errors) == 1


def test_invalid_price_parses_as_none_rather_than_guessed():
    content = "Name,Price\nWidget,not-a-number\n"
    result = parse_csv(content)
    assert result.rows[0].buy_price is None


def test_missing_name_column_reports_error():
    content = "Foo,Bar\n1,2\n"
    result = parse_csv(content)
    assert result.rows == []
    assert "name column" in result.errors[0]
