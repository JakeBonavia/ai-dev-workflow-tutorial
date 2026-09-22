import pandas as pd
import pytest

import analytics

SAMPLE_ROWS = [
    {"date": "2024-01-01", "order_id": "ORD-001", "product": "Widget A", "category": "Electronics", "region": "North", "quantity": 1, "unit_price": 100, "total_amount": 100},
    {"date": "2024-01-01", "order_id": "ORD-002", "product": "Widget B", "category": "Accessories", "region": "South", "quantity": 1, "unit_price": 50,  "total_amount": 50},
    {"date": "2024-01-02", "order_id": "ORD-003", "product": "Widget A", "category": "Electronics", "region": "South", "quantity": 1, "unit_price": 200, "total_amount": 200},
    {"date": "2024-01-02", "order_id": "ORD-004", "product": "Widget C", "category": "Audio",       "region": "North", "quantity": 1, "unit_price": 30,  "total_amount": 30},
    {"date": "2024-01-03", "order_id": "ORD-005", "product": "Widget B", "category": "Accessories", "region": "North", "quantity": 1, "unit_price": 70,  "total_amount": 70},
    {"date": "2024-01-03", "order_id": "ORD-006", "product": "Widget C", "category": "Audio",       "region": "South", "quantity": 1, "unit_price": 40,  "total_amount": 40},
    {"date": "2024-01-03", "order_id": "ORD-007", "product": "Widget A", "category": "Electronics", "region": "North", "quantity": 1, "unit_price": 150, "total_amount": 150},
    {"date": "2024-01-04", "order_id": "ORD-008", "product": "Widget B", "category": "Accessories", "region": "South", "quantity": 1, "unit_price": 60,  "total_amount": 60},
    {"date": "2024-01-04", "order_id": "ORD-009", "product": "Widget C", "category": "Audio",       "region": "North", "quantity": 1, "unit_price": 20,  "total_amount": 20},
    {"date": "2024-01-05", "order_id": "ORD-010", "product": "Widget A", "category": "Electronics", "region": "South", "quantity": 1, "unit_price": 80,  "total_amount": 80},
]


@pytest.fixture
def sample_df():
    df = pd.DataFrame(SAMPLE_ROWS)
    df["date"] = pd.to_datetime(df["date"])
    return df


def test_load_sales_data_valid(tmp_path):
    csv_path = tmp_path / "sales.csv"
    pd.DataFrame(SAMPLE_ROWS).to_csv(csv_path, index=False)

    df = analytics.load_sales_data(str(csv_path))

    assert len(df) == 10
    assert analytics.REQUIRED_COLUMNS.issubset(set(df.columns))
    assert pd.api.types.is_datetime64_any_dtype(df["date"])


def test_load_sales_data_missing_column(tmp_path):
    csv_path = tmp_path / "sales.csv"
    incomplete_rows = [{k: v for k, v in row.items() if k != "region"} for row in SAMPLE_ROWS]
    pd.DataFrame(incomplete_rows).to_csv(csv_path, index=False)

    with pytest.raises(ValueError):
        analytics.load_sales_data(str(csv_path))
