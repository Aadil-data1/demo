import pandas as pd

customers = pd.DataFrame({
    "Customer_ID": [101, 102, 103],
    "Name": ["Aadi", "Sara", "Rahul"],
    "City": ["Delhi", "Mumbai", "Chennai"]
})

orders = pd.DataFrame({
    "Order_ID": [1, 2, 3, 4],
    "Customer_ID": [101, 102, 101, 104],
    "Amount": [500, 800, 300, 900]
})

combined = pd.merge(
    orders,
    customers,
    on="Customer_ID",
    how= "outer"
)
january = pd.DataFrame({
    "Product": ["Laptop", "Phone"],
    "Sales": [50000, 30000]
})

february = pd.DataFrame({
    "Product": ["Laptop", "Tablet"],
    "Sales": [60000, 20000]
})

all_sales = pd.concat(
    [january, february],
    ignore_index=True
)

names = pd.DataFrame({
    "Name": ["Aadi", "Sara", "Rahul"]
})

scores = pd.DataFrame({
    "Marks": [85, 92, 78]
})

combined = pd.concat(
    [names, scores],
    axis= 1
)

print(combined)