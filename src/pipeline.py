
from src.ingestion.fetch_products import fetch_products
from src.transformation.clean_products import clean_products
from src.database.load_products import load_products
from src.analytics.product_report import run_report


def main():
    print("\nSTEP 1: Fetching product data")
    fetch_products()

    print("\nSTEP 2: Cleaning product data")
    clean_products()

    print("\nSTEP 3: Loading products into SQLite")
    load_products()

    print("\nSTEP 4: Running analytics")
    run_report()

    print("\nPipeline completed successfully.")


if __name__ == "__main__":
    main()
