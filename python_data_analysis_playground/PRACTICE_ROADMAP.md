# NumPy + pandas practice roadmap

Work through these sections in order. Try each task yourself before looking up syntax. Use `retail_transactions.csv` as the default dataset unless another file is named.

## 1. Loading, inspecting and understanding data
**Files:** all tables

- `pd.read_csv()`, `head()`, `tail()`, `sample()`, `shape`, `columns`, `index`, `dtypes`, `info()`, `describe()`, `memory_usage()`.
- `value_counts()`, `nunique()`, `unique()`, `select_dtypes()`, `is_numeric_dtype()`.
- Questions: How many rows and columns are in each table? Which columns are numeric, categorical, dates or identifiers? Which columns have missing values?

## 2. Selecting rows and columns
**File:** `retail_transactions.csv`, `customers.csv`

- Column selection, lists of columns, `.loc`, `.iloc`, boolean masks, `isin()`, `between()`, `query()`, `at`, `iat`, `where()`, `mask()`.
- Questions: Find delivered orders from one city; select products within a price range; find customers whose satisfaction score is missing.

## 3. NumPy foundations and vectorized calculations
**Files:** `products.csv`, `retail_transactions.csv`

- `np.array`, `shape`, `ndim`, `dtype`, `astype`, `arange`, `linspace`, `zeros`, `ones`, `full`, `eye`, `reshape`, `ravel`, `flatten`, `transpose`, `squeeze`, `concatenate`, `stack`, `vstack`, `hstack`, `split`.
- Math: `sum`, `mean`, `median`, `std`, `var`, `min`, `max`, `ptp`, `percentile`, `quantile`, `round`, `floor`, `ceil`, `sqrt`, `log`, `exp`, `clip`, `isfinite`, `isnan`.
- Logic and selection: comparisons, boolean masks, `where`, `select`, `all`, `any`, `nonzero`, `argmin`, `argmax`, `argsort`, `sort`, `unique`, `bincount`, `count_nonzero`.
- Randomness and sampling: `default_rng`, `integers`, `choice`, `normal`, `uniform`, `permutation`, `shuffle`, `seed` concepts.
- Broadcasting: calculate margins or discount amounts for arrays of many products; explain the shapes before doing the calculation.
- Questions: Which products have the highest gross margin? What is the 90th percentile order-line value? Flag values above a threshold using `np.where()`.

## 4. Arithmetic, derived columns and functions
**File:** `retail_transactions.csv`

- Vectorized operators, `.add()`, `.sub()`, `.mul()`, `.div()`, `.round()`, `.clip()`, `.abs()`, `.pow()`, `.eval()`, `.assign()`, `apply()`, `map()`, `replace()`, `pipe()`.
- Questions: Calculate margin amount and margin percentage, classify order lines, compute a discount band, create a high-value flag.

## 5. Sorting, ranking and top-N analysis
**Files:** `products.csv`, `employees.csv`, `retail_transactions.csv`

- `sort_values()`, `sort_index()`, `nlargest()`, `nsmallest()`, `rank()`, `idxmax()`, `idxmin()`, `duplicated()`.
- Questions: Find the 10 most expensive products; rank employees by salary within a department; identify the customers with the most purchase lines.

## 6. Missing data and data quality
**Files:** `messy_sales.csv`, `customers.csv`, `survey_responses.csv`

- `isna()`, `notna()`, `dropna()`, `fillna()`, `ffill()`, `bfill()`, `interpolate()`, `drop_duplicates()`, `duplicated()`, `replace()`, `astype()`, `convert_dtypes()`, `pd.to_numeric(errors="coerce")`, `pd.to_datetime(errors="coerce")`.
- Questions: Standardize city names; convert sales strings to numbers; identify invalid dates; decide which missing values should be dropped, filled or left missing. Explain why each choice is defensible.

## 7. String operations and text cleaning
**Files:** `customers.csv`, `messy_sales.csv`, `survey_responses.csv`

- `.str.lower()`, `.str.upper()`, `.str.title()`, `.str.strip()`, `.str.contains()`, `.str.startswith()`, `.str.endswith()`, `.str.replace()`, `.str.split()`, `.str.extract()`, `.str.len()`, `.str.pad()`, `.str.match()`.
- Questions: normalize city and category labels; identify comments mentioning delivery; extract the email domain; clean inconsistent coupon values.

## 8. Dates and times
**Files:** `orders.csv`, `website_events.csv`, `daily_regional_metrics.csv`

- `pd.to_datetime()`, `.dt.year`, `.dt.month`, `.dt.day`, `.dt.day_name()`, `.dt.dayofweek`, `.dt.quarter`, `.dt.is_month_end`, `.dt.days_in_month`, date subtraction, `Timedelta`, `DateOffset`, `Period`, `PeriodIndex`, `DateTimeIndex`, `resample()`.
- Questions: Calculate delivery duration; compare weekday and weekend sales; aggregate to month and quarter; find the busiest hour of day in website events.

## 9. Grouping and aggregation
**Files:** `retail_transactions.csv`, `employees.csv`, `inventory_movements.csv`

- `groupby()`, `agg()`, `transform()`, `filter()`, `size()`, `count()`, `sum()`, `mean()`, `median()`, `min()`, `max()`, `std()`, `nunique()`, named aggregation, multiple grouping keys.
- Questions: revenue by category; average salary by department; inventory change by product and warehouse; normalize each employee's salary against their own department's average with `transform()`.

## 10. Combining data: joins and concatenation
**Files:** customers, orders, order_items, products, inventory

- `merge()` with `inner`, `left`, `right`, and `outer`; `validate`; `indicator`; `suffixes`; `join()`; `concat()` along rows and columns; `keys`; index alignment.
- Questions: attach customer attributes to orders; find customers with no orders; check whether every order item references a valid product; combine monthly extracts.

## 11. Reshaping tables
**Files:** `retail_transactions.csv`, `daily_regional_metrics.csv`

- `pivot()`, `pivot_table()`, `melt()`, `stack()`, `unstack()`, `wide_to_long()`, `crosstab()`, `explode()`, `get_dummies()`, `factorize()`.
- Questions: make a region-by-month revenue grid; compare average product sales by city; reshape a wide summary into tidy long format; produce a category-by-channel count table.

## 12. Time-series analysis
**File:** `daily_regional_metrics.csv`

- Set a datetime index, `resample()`, `asfreq()`, `reindex()`, `rolling()`, `expanding()`, `ewm()`, `shift()`, `diff()`, `pct_change()`, `cumsum()`, `cumprod()`, `cummin()`, `cummax()`, `to_period()`.
- Questions: calculate a 7-day moving average; compare daily revenue with the previous week; calculate monthly region totals and cumulative revenue; restore missing calendar dates before filling them thoughtfully.

## 13. Statistics and relationships
**Files:** `retail_transactions.csv`, `employees.csv`, `daily_regional_metrics.csv`

- `corr()`, `cov()`, `quantile()`, `value_counts(normalize=True)`, `describe()`, `corrwith()`, `mode()`, `sem()`, `skew()`, `kurt()`, `cut()`, `qcut()`.
- Questions: study how discount relates to quantity; compare salary distributions by department; create quartile groups for order values. Remember correlation does not establish causation.

## 14. Indexing and alignment concepts
**Any DataFrame**, especially `customers.csv` and `orders.csv`

- `set_index()`, `reset_index()`, `reindex()`, `rename_axis()`, `rename()`, `droplevel()`, `swaplevel()`, `sort_index()`, `.align()`, `combine_first()`, MultiIndex grouping and selection.
- Questions: index orders by ID; create a customer-month MultiIndex summary; inspect how pandas aligns rows when adding two Series with different indexes.

## 15. Categories, encoding and frequency analysis
**Files:** `customers.csv`, `products.csv`, `website_events.csv`, `survey_responses.csv`

- `astype("category")`, `.cat.categories`, `.cat.codes`, `.cat.set_categories()`, `get_dummies()`, `factorize()`, `crosstab()`, `value_counts()`.
- Questions: order loyalty tiers logically; encode category variables; compare traffic sources across devices.

## 16. Files, exports and reproducible workflows
**All tables**

- `to_csv()`, `read_csv()` options such as `usecols`, `dtype`, `parse_dates`, `na_values`, `chunksize`; `to_json()`, `read_json()`, `to_excel()`/`read_excel()` where Excel support is installed; pickle only for trusted local workflows.
- Questions: save a cleaned table; export a pivot to CSV; read only selected columns; process the larger events table in chunks.

## 17. Integrated mini-projects

1. **Retail performance:** category and city revenue, average order value, discounts, and return patterns. Avoid double-counting order-level totals in the line-level flat table.
2. **Customer behaviour:** acquisition channel, loyalty tier, repeat purchase frequency and satisfaction.
3. **Website funnel:** event counts through product views, cart, checkout and purchase by device and traffic source.
4. **Inventory control:** cumulative stock change by product/warehouse, damaged goods and frequent adjustments.
5. **People analytics:** department salary comparisons, tenure and performance relationships. Treat simulated results as practice only.
6. **Dirty data rescue:** take `messy_sales.csv` from raw input to a documented, validated clean table.
7. **Time-series report:** daily to weekly/monthly resampling, rolling averages, missing dates and region comparisons.

## A useful habit

For every function you practise, write four things: (1) what problem it solves, (2) what input shape it expects, (3) what output it returns, and (4) one small example from this dataset. This builds understanding rather than memorizing function names.
