import numpy as np
import pandas as pd

rng = np.random.default_rng(7)  # fixed seed: same data every run

cities = ["New York", "London", "Mumbai", "Tokyo", "Toronto"]
products = ["Laptop", "Phone", "Tablet", "Headphones", "Smartwatch"]

n = 200
df = pd.DataFrame({
    "city": rng.choice(cities, n),
    "product": rng.choice(products, n),
    "sales": rng.integers(100, 5000, n),
})

df.to_csv("sales_data.csv", index=False)

# Confirm there are no nulls
assert df.isna().sum().sum() == 0
print(df.describe())