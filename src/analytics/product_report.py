
import sqlite3
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATABASE_PATH = PROJECT_ROOT / "data" / "ecommerce.db"


def run_report():
    """Run product inventory and category analytics."""

    with sqlite3.connect(DATABASE_PATH) as connection:

        print("\n=== 1. PRODUCTS WITH LOWEST STOCK ===")

        low_stock = connection.execute("""
            SELECT title, category, stock
            FROM products
            ORDER BY stock ASC
            LIMIT 5
        """).fetchall()

        for title, category, stock in low_stock:
            print(f"{title} | {category} | Stock: {stock}")

        print("\n=== 2. PRODUCTS PER CATEGORY ===")

        categories = connection.execute("""
            SELECT category, COUNT(*) AS product_count
            FROM products
            GROUP BY category
            ORDER BY product_count DESC, category ASC
        """).fetchall()

        for category, count in categories:
            print(f"{category}: {count} products")

        print("\n=== 3. AVERAGE PRICE PER CATEGORY ===")

        average_prices = connection.execute("""
            SELECT category, ROUND(AVG(price), 2) AS average_price
            FROM products
            GROUP BY category
            ORDER BY average_price DESC
        """).fetchall()

        for category, average_price in average_prices:
            print(f"{category}: {average_price:.2f}")


if __name__ == "__main__":
    run_report()
