# Python Data Analysis Playground

A reusable, synthetic data collection designed for practising Python's NumPy and pandas libraries without continually searching for new datasets.

## Start here

**Open `data/retail_transactions.csv` first.** It is a wide, ready-to-analyse table combining order items with order, product and customer attributes. It is the easiest file for your first experiments with filtering, arithmetic, NumPy arrays, sorting, grouping, aggregation, missing values, strings and charts.

When you are ready for real relational-data practice, use `customers.csv`, `products.csv`, `orders.csv` and `order_items.csv` separately and join them with `merge()`.

All records are synthetic and fictional. They do not describe real customers, staff, or transactions. The random seed is fixed in `generate_dataset.py`, so you can regenerate the same data.

## Files at a glance

| File | Main practice opportunities |
|---|---|
| `retail_transactions.csv` | Single-table analysis; arithmetic, masks, groupby, aggregation, sorting, ranking, correlations, plotting |
| `customers.csv` | Strings, categories, missing values, filtering, `value_counts`, mapping, customer segmentation |
| `products.csv` | Numeric summaries, categories, sorting, `where`, `select`, arrays, price/cost calculations |
| `orders.csv` | Dates, time differences, statuses, conditional columns, date parts, groupby and order-level summaries |
| `order_items.csv` | Line-level totals, multiple rows per order, duplicates checks, joins and reshaping |
| `website_events.csv` | High-volume event data, datetimes, sessions, event frequencies, conversion analysis |
| `daily_regional_metrics.csv` | Time series, missing dates, `resample`, rolling windows, shifts, cumulative calculations, trends |
| `inventory_movements.csv` | Positive/negative values, stock changes, grouping and cumulative totals |
| `employees.csv` | Department summaries, salary distributions, ranking, quantiles, correlations and date calculations |
| `survey_responses.csv` | Ordinal ratings, text methods, missing data, NPS-style summaries and categories |
| `messy_sales.csv` | Deliberately dirty data for `isna`, `dropna`, `fillna`, `duplicated`, `drop_duplicates`, `to_numeric`, `to_datetime`, `str` methods and outlier detection |
| `data_dictionary.csv` | Column names, example data types, sample values and brief descriptions |
| `VISUALIZATION_PRACTICE.md` | Matplotlib and Seaborn chart ideas with starter examples |

## Loading the files

```python
import numpy as np
import pandas as pd
from pathlib import Path

DATA = Path("data")  # Run your notebook from this project folder
transactions = pd.read_csv(DATA / "retail_transactions.csv", parse_dates=["order_date", "ship_date", "delivery_date", "signup_date"])
customers = pd.read_csv(DATA / "customers.csv", parse_dates=["signup_date"])
products = pd.read_csv(DATA / "products.csv", parse_dates=["launch_date"])
orders = pd.read_csv(DATA / "orders.csv", parse_dates=["order_date", "ship_date", "delivery_date", "promised_delivery_date"])
items = pd.read_csv(DATA / "order_items.csv")
daily = pd.read_csv(DATA / "daily_regional_metrics.csv", parse_dates=["date"])
events = pd.read_csv(DATA / "website_events.csv", parse_dates=["event_timestamp"])
```

If a relative path does not work, print `Path.cwd()` to see your current working directory, or use the full path to the `data` folder. In VS Code, place your notebook or `.py` file in this project folder.

## Important data notes

- IDs such as `C00001` and `P0001` are text identifiers, not numbers to calculate with.
- In `retail_transactions.csv`, a single order may appear on multiple rows because each row represents one line item. Do not sum `order_total` across this table unless you first reduce to one row per order; otherwise the order total will be repeated once for every item.
- `net_sales` is line-item sales after its line discount. `order_total` includes item sales, shipping and tax. The fields are intentionally distinct.
- The primary business tables are mostly structured and suitable for analytical practice. `messy_sales.csv` is intentionally untidy. Some tables also contain a modest amount of missing optional data.
- A small proportion of daily dates are missing in `daily_regional_metrics.csv` so you can practise reindexing and resampling.
- A few domain details are simulated for learning and should not be treated as real business facts.

## NumPy and pandas practice map

The accompanying `PRACTICE_ROADMAP.md` maps a broad range of commonly used NumPy and pandas operations to these tables. `VISUALIZATION_PRACTICE.md` adds Matplotlib and Seaborn chart exercises. No finite dataset can meaningfully exercise literally every function in either library—specialized functions exist for image arrays, linear algebra, sparse matrices, geospatial data, and more—but this collection covers a broad range of practical data-analysis workflows.
