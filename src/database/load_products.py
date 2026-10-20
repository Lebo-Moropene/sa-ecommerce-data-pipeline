
import sqlite3
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

CSV_PATH = PROJECT_ROOT / "data" / "processed" / "clean_products.csv"
DATABASE_PATH = PROJECT_ROOT / "data" / "ecommerce.db"


def load_products():
    """Load clean product data into a SQLite database."""

    if not CSV_PATH.exists():
        raise FileNotFoundError(
            f"Clean CSV not found: {CSV_PATH}. Run the cleaning step first."
        )

    df = pd.read_csv(CSV_PATH)

    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DATABASE_PATH) as connection:
        df.to_sql("products", connection, if_exists="replace", index=False)

        count = connection.execute(
            "SELECT COUNT(*) FROM products"
        ).fetchone()[0]

    print(f"Products loaded into database: {count}")
    print(f"Database saved to: {DATABASE_PATH}")


if __name__ == "__main__":
    load_products()
