import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
df = pd.read_csv("daily_sales.csv")
#print(df.head())
#print(df.shape)
#print(df.columns)
#df.info()
#print(df.isna().sum())
missing_percent = (df.isna().mean() * 100).round(2)

#print(missing_percent)
#print("Duplicate rows:", df.duplicated().sum())
#print(df.dtypes)
df["date"] = pd.to_datetime(
   df["date"],
   errors="coerce"
)
#print(df.dtypes)
#print(df["sales"].mean())
#print(df["sales"].describe())
sns.histplot(
    data=df,
    x="sales",
    bins=20
)

plt.title("Distribution of Sales")
plt.xlabel("Sales amount")
plt.ylabel("Number of records")

plt.tight_layout()
plt.show()

largest_sales = df.sort_values(
    "sales",
    ascending=False
).head(10)

print(largest_sales)