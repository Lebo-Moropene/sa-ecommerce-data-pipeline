
import json
from pathlib import Path

import requests


API_URL = "https://dummyjson.com/products?limit=10"

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "products_api.json"


def fetch_products():
    """Fetch product records from the public sample API."""
    try:
        response = requests.get(API_URL, timeout=(5, 15))
        response.raise_for_status()
        payload = response.json()

    except requests.RequestException as error:
        raise SystemExit(f"HTTP request failed: {error}") from error
    except ValueError as error:
        raise SystemExit(f"API returned invalid JSON: {error}") from error

    if not isinstance(payload, dict):
        raise SystemExit("Unexpected API response: expected a JSON object.")

    products = payload.get("products")

    if not isinstance(products, list):
        raise SystemExit("Unexpected API response: products list is missing.")

    RAW_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)

    with RAW_DATA_PATH.open("w", encoding="utf-8") as file:
        json.dump(payload, file, indent=2, ensure_ascii=False)

    print(f"HTTP status: {response.status_code}")
    print(f"Products retrieved: {len(products)}")
    print(f"Total products reported by API: {payload.get('total')}")
    print(f"Raw data saved to: {RAW_DATA_PATH}")


if __name__ == "__main__":
    fetch_products()
