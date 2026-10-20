
import json
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "products_api.json"
PROCESSED_DATA_PATH = PROJECT_ROOT / "data" / "processed" / "clean_products.csv"
REJECTED_DATA_PATH = PROJECT_ROOT / "data" / "rejected" / "rejected_products.csv"


def clean_products():
    """Validate product records and save clean and rejected records."""

    with RAW_DATA_PATH.open("r", encoding="utf-8") as file:
        payload = json.load(file)

    products = payload["products"]
    df = pd.DataFrame(products)

    required_columns = ["id", "title", "category", "price", "stock"]

    for column in required_columns:
        if column not in df.columns:
            raise ValueError(f"Required column is missing: {column}")

    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df["stock"] = pd.to_numeric(df["stock"], errors="coerce")

    invalid_rows = (
        df["id"].isna()
        | df["title"].isna()
        | df["title"].astype(str).str.strip().eq("")
        | df["category"].isna()
        | df["price"].isna()
        | df["stock"].isna()
        | (df["price"] < 0)
        | (df["stock"] < 0)
        | df["id"].duplicated(keep="first")
    )

    rejected = df[invalid_rows].copy()
    clean = df[~invalid_rows].copy()

    clean = clean[
        ["id", "title", "category", "brand", "price", "stock", "rating"]
    ].copy()

    clean["brand"] = clean["brand"].fillna("Unknown")
    clean["rating"] = pd.to_numeric(clean["rating"], errors="coerce")

    PROCESSED_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    REJECTED_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)

    clean.to_csv(PROCESSED_DATA_PATH, index=False)
    rejected.to_csv(REJECTED_DATA_PATH, index=False)

    print(f"Products received: {len(df)}")
    print(f"Clean products: {len(clean)}")
    print(f"Rejected products: {len(rejected)}")
    print(f"Clean data saved to: {PROCESSED_DATA_PATH}")
    print(f"Rejected data saved to: {REJECTED_DATA_PATH}")


if __name__ == "__main__":
    clean_products()
