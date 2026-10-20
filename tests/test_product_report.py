
import sqlite3

import pytest


@pytest.fixture
def database():
    connection = sqlite3.connect(":memory:")

    connection.execute("""
        CREATE TABLE products (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER NOT NULL
        )
    """)

    connection.executemany(
        """
        INSERT INTO products (id, title, category, price, stock)
        VALUES (?, ?, ?, ?, ?)
        """,
        [
            (1, "Product A", "beauty", 10.0, 5),
            (2, "Product B", "beauty", 20.0, 15),
            (3, "Product C", "fragrances", 60.0, 2),
        ],
    )

    yield connection
    connection.close()


def test_products_are_counted_by_category(database):
    results = database.execute("""
        SELECT category, COUNT(*)
        FROM products
        GROUP BY category
        ORDER BY category
    """).fetchall()

    assert results == [
        ("beauty", 2),
        ("fragrances", 1),
    ]


def test_lowest_stock_product_is_returned_first(database):
    results = database.execute("""
        SELECT title, stock
        FROM products
        ORDER BY stock ASC
        LIMIT 1
    """).fetchall()

    assert results == [("Product C", 2)]


def test_average_price_is_calculated_correctly(database):
    result = database.execute("""
        SELECT AVG(price)
        FROM products
        WHERE category = 'beauty'
    """).fetchone()[0]

    assert result == pytest.approx(15.0)
