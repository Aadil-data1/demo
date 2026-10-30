# Visualization practice: Matplotlib + Seaborn

The same dataset can support many chart types. The purpose is not to make every chart, but to choose the chart that best answers a question and learn how the plotting functions map data to visual form.

Load the tools and data:

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

DATA = "data"
transactions = pd.read_csv(f"{DATA}/retail_transactions.csv", parse_dates=["order_date"])
products = pd.read_csv(f"{DATA}/products.csv")
daily = pd.read_csv(f"{DATA}/daily_regional_metrics.csv", parse_dates=["date"])
employees = pd.read_csv(f"{DATA}/employees.csv", parse_dates=["hire_date"])
events = pd.read_csv(f"{DATA}/website_events.csv", parse_dates=["event_timestamp"])
```

## Chart practice map

| Question | Best file | Try these charts/functions | What to explore |
|---|---|---|---|
| How does revenue change over time? | `daily_regional_metrics.csv` | Matplotlib `plot`; Seaborn `lineplot` | Daily noise, 7-day rolling average, region comparisons, monthly resampling |
| Which categories generate the most sales? | `retail_transactions.csv` | `bar`, `barplot`, `catplot` | Aggregate first; sort categories by total `net_sales` |
| How are order-line sales distributed? | `retail_transactions.csv` | `hist`, `histplot`, `kdeplot` | Skew, bins, mean/median, whether a log scale helps |
| Are there unusually high values? | `retail_transactions.csv`, `messy_sales.csv` | `boxplot`, `boxenplot`, `stripplot` | Quartiles, outliers, and why a flagged point is not automatically an error |
| Does discount relate to quantity or sales? | `retail_transactions.csv` | `scatter`, `scatterplot`, `regplot`, `jointplot` | Relationships, overplotting, subgroups, correlation versus causation |
| Do salary distributions differ by department? | `employees.csv` | `boxplot`, `violinplot`, `stripplot` | Median, spread, small group sizes and overlapping distributions |
| What does a category-by-channel comparison look like? | `retail_transactions.csv` | `pivot_table` + `heatmap` | Decide whether cells should show sum, mean or count before drawing |
| Which event types are common? | `website_events.csv` | `value_counts()` + `barplot`, `countplot` | Counts versus percentages; compare devices with hue/facets |
| Is there a relationship among many numeric variables? | `daily_regional_metrics.csv`, `employees.csv` | `corr()` + `heatmap`; Seaborn `pairplot` | Correlation coefficients, scales, missing values and redundant variables |
| Are weekdays different from weekends? | `daily_regional_metrics.csv` | `boxplot`, `violinplot`, `pointplot` | Derive weekday/weekend labels and compare the full distributions |
| How does satisfaction vary by loyalty tier? | `customers.csv`, `survey_responses.csv` | `barplot`, `boxplot`, `countplot` | Ordinal scores, missing values and sample sizes |
| Does event activity vary by hour? | `website_events.csv` | `dt.hour`, grouped line/bar chart | Create hour-of-day and day-of-week columns from `event_timestamp` |

## A few starter examples

### 1. Matplotlib line chart

```python
north = daily.loc[daily["region"] == "North"].sort_values("date")
north = north.assign(revenue_7d=north["revenue"].rolling(7).mean())

plt.figure(figsize=(10, 4))
plt.plot(north["date"], north["revenue"], label="Daily revenue", alpha=0.5)
plt.plot(north["date"], north["revenue_7d"], label="7-day average")
plt.xlabel("Date")
plt.ylabel("Revenue")
plt.title("North region revenue over time")
plt.legend()
plt.tight_layout()
plt.show()
```

### 2. Seaborn distribution plot

```python
sns.histplot(data=transactions, x="net_sales", bins=40, kde=True)
plt.title("Distribution of order-line net sales")
plt.tight_layout()
plt.show()
```

### 3. Seaborn boxplot

```python
sns.boxplot(data=employees, x="department", y="salary_inr")
plt.xticks(rotation=35, ha="right")
plt.title("Salary distribution by department")
plt.tight_layout()
plt.show()
```

### 4. Heatmap from a pandas pivot table

```python
sales_grid = transactions.pivot_table(
    index="category", columns="sales_channel", values="net_sales", aggfunc="sum", fill_value=0
)
sns.heatmap(sales_grid, annot=False)
plt.title("Net sales by category and sales channel")
plt.tight_layout()
plt.show()
```

## Visualization habits worth learning

1. Aggregate at the right level before plotting. `retail_transactions.csv` has one row per order item, so order-level columns repeat when an order has multiple items.
2. Label axes with meaningful units, include an informative title, and use legends only when they clarify the chart.
3. Start with a simple chart; add hue, facets, annotations or a trend line only when they answer a real question.
4. A chart can reveal patterns, but it cannot by itself prove why a pattern happened.
