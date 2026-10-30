import pandas as pd
import numpy as np
import time

rng = np.random.default_rng(42)

df = pd.DataFrame({
    "Quantity": rng.integers(1, 10, size=100_000),
    "Price": rng.integers(100, 10_000, size=100_000)
})

df.to_csv("transction_records.csv", index= False) 

print(df.head())
print(df.shape)