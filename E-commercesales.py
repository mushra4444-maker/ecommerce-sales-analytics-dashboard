
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Load your dataset
file_path = Path(
    r"C:\Users\mushr\Downloads\powerbi excel(Sheet1).csv"
)

df = pd.read_csv(file_path)

# Clean column names and remove duplicate sales
df.columns = df.columns.str.strip()
df = df.drop_duplicates(subset=["SaleID"])

# Convert columns to correct data types
df["Date"] = pd.to_datetime(
    df["Date"], format="mixed", dayfirst=False, errors="coerce"
)
df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
df["UnitPrice"] = pd.to_numeric(df["UnitPrice"], errors="coerce")

df = df.dropna(
    subset=["Date", "Quantity", "UnitPrice"]
)

# Add product names and categories where known
product_names = {
    "P001": "Laptop",
    "P002": "Mouse",
    "P003": "Keyboard",
    "P004": "Monitor"
}

product_categories = {
    "P001": "Electronics",
    "P002": "Accessories",
    "P003": "Accessories",
    "P004": "Electronics"
}

df["Product"] = df["ProductID"].map(product_names).fillna(df["ProductID"])
df["Category"] = df["ProductID"].map(product_categories).fillna("Other")

# Calculate sales revenue
df["Revenue"] = df["Quantity"] * df["UnitPrice"]

# Add month for trend analysis
df["Month"] = df["Date"].dt.to_period("M").astype(str)

# Display important business KPIs
print("\n--- E-COMMERCE SALES ANALYTICS ---")
print("Total Sales:", round(df["Revenue"].sum(), 2))
print("Total Orders:", df["SaleID"].nunique())
print("Unique Customers:", df["CustomerID"].nunique())
print("Units Sold:", df["Quantity"].sum())
print("Average Order Value:",
      round(df["Revenue"].sum() / df["SaleID"].nunique(), 2))

# Revenue by city
city_sales = (
    df.groupby("City", as_index=False)["Revenue"]
    .sum()
    .sort_values("Revenue", ascending=False)
)
print("\nRevenue by City:")
print(city_sales)

# Revenue by product
product_sales = (
    df.groupby("Product", as_index=False)["Revenue"]
    .sum()
    .sort_values("Revenue", ascending=False)
)
print("\nRevenue by Product:")
print(product_sales)

# Monthly revenue
monthly_sales = (
    df.groupby("Month", as_index=False)["Revenue"]
    .sum()
    .sort_values("Month")
)
print("\nMonthly Revenue:")
print(monthly_sales)

# Save outputs
output_dir = Path(__file__).resolve().parent / "output"
output_dir.mkdir(exist_ok=True)

df.to_csv(output_dir / "cleaned_sales.csv", index=False)
city_sales.to_csv(output_dir / "city_sales.csv", index=False)
product_sales.to_csv(output_dir / "product_sales.csv", index=False)
monthly_sales.to_csv(output_dir / "monthly_sales.csv", index=False)

# Chart 1: Monthly revenue
plt.figure(figsize=(10, 5))
plt.plot(
    monthly_sales["Month"],
    monthly_sales["Revenue"],
    marker="o"
)
plt.title("Monthly E-commerce Revenue")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(output_dir / "monthly_revenue.png")
plt.show()

# Chart 2: Revenue by city
plt.figure(figsize=(9, 5))
plt.bar(city_sales["City"], city_sales["Revenue"])
plt.title("Revenue by City")
plt.xlabel("City")
plt.ylabel("Revenue")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig(output_dir / "city_revenue.png")
plt.show()

print("\nAnalysis completed! Check the output folder.")
