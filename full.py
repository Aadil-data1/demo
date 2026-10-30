from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Locate the folder containing this Python script.
PROJECT_DIR = Path(__file__).resolve().parent

# Define the input file and output folders.
CSV_PATH = PROJECT_DIR / "sales.csv"
OUTPUT_DIR = PROJECT_DIR / "outputs"
TABLE_DIR = OUTPUT_DIR / "tables"
FIGURE_DIR = OUTPUT_DIR / "figures"

# Create the output folders if they do not already exist.
TABLE_DIR.mkdir(parents=True, exist_ok=True)
FIGURE_DIR.mkdir(parents=True, exist_ok=True)

# Load the original dataset.
raw_df = pd.read_csv(CSV_PATH)

# Create a separate working copy.
df = raw_df.copy()

print(df.head())
print("Dataset shape:", df.shape)
df.info()