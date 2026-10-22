# SA E-Commerce Data Pipeline

A Python data engineering pipeline that extracts product data from a public
REST API, validates and cleans it, loads it into a SQLite data store, and runs
inventory analytics on the result. The source catalogue is the
computer-electronics slice of the API: laptops, tablets and mobile
accessories.

## Project Overview

The project demonstrates a complete Extract -> Validate -> Transform -> Load ->
Analyse (ETL) workflow for an e-commerce product catalogue, built around a
South African retail scenario.

**Business problems addressed:**

- Identifying products with the lowest stock for replenishment.
- Understanding product mix across categories.
- Comparing average price points between categories.
- Supporting data-driven inventory decisions with reproducible SQL analytics.

## Technology Stack

| Layer | Tool |
| --- | --- |
| Language | Python 3.10+ |
| Ingestion | `requests` (REST API) |
| Transformation | `pandas` |
| Storage | SQLite |
| Analytics | SQL |
| Testing | `pytest` |
| Version control | Git / GitHub |

## Pipeline Architecture

```
dummyjson.com/products/category/* API
        |
        v
[1] Extract   src/ingestion/fetch_products.py    -> data/raw/products_api.json
        |
        v
[2] Validate  src/transformation/clean_products.py
              -> data/processed/clean_products.csv
              -> data/rejected/rejected_products.csv
        |
        v
[3] Load      src/database/load_products.py      -> data/ecommerce.db (products)
        |
        v
[4] Analyse   src/analytics/product_report.py    -> console report
```

`src/pipeline.py` orchestrates all four steps.

## Project Structure

```
.
├── data/
│   ├── raw/            # API responses (gitignored)
│   ├── processed/      # cleaned CSV output (gitignored)
│   ├── rejected/       # rows that failed validation (gitignored)
│   └── ecommerce.db    # SQLite database (gitignored)
├── docs/               # project documentation
├── logs/               # pipeline logs
├── sql/                # ad-hoc SQL queries
├── src/
│   ├── ingestion/      # API extraction
│   ├── transformation/ # validation and cleaning
│   ├── database/       # SQLite loading
│   ├── analytics/      # reporting queries
│   └── pipeline.py     # end-to-end orchestrator
├── tests/              # pytest suite
├── requirements.txt
└── README.md
```

## Usage

### 1. Clone and set up

```bash
git clone git@github.com:Lebo-Moropene/sa-ecommerce-data-pipeline.git
cd sa-ecommerce-data-pipeline

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Run the full pipeline

```bash
python -m src.pipeline
```

Expected output (abridged):

```
STEP 1: Fetching product data
HTTP status: 200 (laptops)
Products retrieved from laptops: 5
HTTP status: 200 (tablets)
Products retrieved from tablets: 3
HTTP status: 200 (mobile-accessories)
Products retrieved from mobile-accessories: 14
Products retrieved: 22

STEP 2: Cleaning product data
Clean products: 22
Rejected products: 0

STEP 3: Loading products into SQLite
Products loaded into database: 22

STEP 4: Running analytics
=== 1. PRODUCTS WITH LOWEST STOCK ===
...
=== 2. PRODUCTS PER CATEGORY ===
...
=== 3. AVERAGE PRICE PER CATEGORY ===
...

Pipeline completed successfully.
```

### 3. Run individual steps

Every module is directly executable:

```bash
python -m src.ingestion.fetch_products
python -m src.transformation.clean_products
python -m src.database.load_products
python -m src.analytics.product_report
```

### 4. Run the tests

```bash
python -m pytest tests/ -v
```

### 5. Query the database yourself

```bash
sqlite3 data/ecommerce.db "SELECT category, AVG(price) FROM products GROUP BY category;"
```

## Data Sources

| Source | Type | Notes |
| --- | --- | --- |
| [dummyjson.com/products/category/laptops](https://dummyjson.com/products/category/laptops) | Public sample REST API | The `laptops`, `tablets` and `mobile-accessories` categories (22 products), 5s connect / 15s read timeout |

Raw, processed and rejected files are written under `data/` and excluded from
version control; only `.gitkeep` placeholders are committed.

## Validation Rules

A record is rejected (written to `data/rejected/rejected_products.csv`) if it:

- is missing `id`, `title`, `category`, `price` or `stock`;
- has a blank or whitespace-only title;
- has a negative `price` or `stock`;
- duplicates a previously seen `id`.

Clean records keep `id`, `title`, `category`, `brand`, `price`, `stock`,
`rating`, with missing brands filled as `Unknown`.

## Analytics Output

1. **Lowest stock** - 5 products closest to running out.
2. **Products per category** - catalogue mix, ordered by count.
3. **Average price per category** - price positioning by category.

## Project Status

- [x] Project scaffolding and version control
- [x] API ingestion with timeouts and error handling
- [x] Validation, cleaning and reject routing
- [x] SQLite load step
- [x] Inventory and category analytics
- [x] Automated tests (`pytest`)
- [x] End-to-end pipeline orchestrator
- [x] README and usage documentation
