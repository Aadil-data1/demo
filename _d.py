import numpy as np
import pandas as pd

np.random.seed(42)
n = 200

# Age: 18–70 (int)
age = np.random.randint(18, 71, size=n)

# Income: positively correlated with age (float)
income = 20000 + (age - 18) * 1200 + np.random.normal(0, 8000, size=n)
income = np.round(np.maximum(income, 15000), 2)

# Purchase amount: positively correlated with income (float)
purchase_amount = 100 + (income - 15000) * 0.03 + np.random.normal(0, 200, size=n)
purchase_amount = np.round(np.maximum(purchase_amount, 50), 2)

df = pd.DataFrame({
    'age': age.astype(int),
    'income': income.astype(float),
    'purchase_amount': purchase_amount.astype(float)
})

df.to_csv('data.csv', index=False)
print(df.head())
print(f"\nCorrelation matrix:\n{df.corr()}")   