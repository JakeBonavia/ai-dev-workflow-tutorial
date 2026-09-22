import pandas as pd

REQUIRED_COLUMNS = {
    "date", "order_id", "product", "category", "region",
    "quantity", "unit_price", "total_amount",
}


def load_sales_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)

    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"sales data is missing required columns: {sorted(missing)}")

    try:
        df["date"] = pd.to_datetime(df["date"])
    except (ValueError, TypeError) as e:
        raise ValueError(f"sales data 'date' column could not be parsed: {e}")

    return df


def total_sales(df: pd.DataFrame) -> float:
    return df["total_amount"].sum()


def total_orders(df: pd.DataFrame) -> int:
    return len(df)


def sales_by_day(df: pd.DataFrame) -> pd.DataFrame:
    result = df.groupby(df["date"].dt.normalize())["total_amount"].sum().reset_index()
    return result.sort_values("date").reset_index(drop=True)


def sales_by_category(df: pd.DataFrame) -> pd.DataFrame:
    result = df.groupby("category")["total_amount"].sum().reset_index()
    return result.sort_values("total_amount", ascending=False).reset_index(drop=True)


def sales_by_region(df: pd.DataFrame) -> pd.DataFrame:
    result = df.groupby("region")["total_amount"].sum().reset_index()
    return result.sort_values("total_amount", ascending=False).reset_index(drop=True)
