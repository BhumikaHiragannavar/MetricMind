import pandas as pd

df = pd.read_csv("../data/superstore.csv")
print(df.columns.tolist())
print(df.head())
print(df.isnull().sum())
print("Total Sales:",df["Sales"].sum())
print("Total Profit:",df["Profit"].sum())
print("Total Quantity:",df["Quantity"].sum())
print("Profit Margin:",(df["Profit"].sum() / df["Sales"].sum()) * 100)
