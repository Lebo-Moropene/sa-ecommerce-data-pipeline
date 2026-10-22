
import json
from pathlib import Path

import requests


API_BASE_URL = "https://dummyjson.com/products/category"
API_CATEGORIES = ["laptops", "tablets", "mobile-accessories"]

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "products_api.json"


def fetch_products():
    """Fetch product records from the public sample API."""
    products = []
    total = 0

    for category in API_CATEGORIES:
        url = f"{API_BASE_URL}/{category}"

        try:
            response = requests.get(url, timeout=(5, 15))
            response.raise_for_status()
            payload = response.json()

        except requests.RequestException as error:
            raise SystemExit(f"HTTP request failed: {error}") from error
        except ValueError as error:
            raise SystemExit(f"API returned invalid JSON: {error}") from error

        if not isinstance(payload, dict):
            raise SystemExit("Unexpected API response: expected a JSON object.")

        category_products = payload.get("products")

        if not isinstance(category_products, list):
            raise SystemExit("Unexpected API response: products list is missing.")

        products.extend(category_products)
        total += payload.get("total", len(category_products))

        print(f"HTTP status: {response.status_code} ({category})")
        print(f"Products retrieved from {category}: {len(category_products)}")

    merged_payload = {
        "products": products,
        "total": total,
        "skip": 0,
        "limit": len(products),
    }

    RAW_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)

    with RAW_DATA_PATH.open("w", encoding="utf-8") as file:
        json.dump(merged_payload, file, indent=2, ensure_ascii=False)

    print(f"Products retrieved: {len(products)}")
    print(f"Total products reported by API: {total}")
    print(f"Raw data saved to: {RAW_DATA_PATH}")


if __name__ == "__main__":
    fetch_products()
