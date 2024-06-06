import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Setting seed as 11 for this one, will change it for the next 5-10 sets to be generated
np.random.seed(11)

# Number of records
num_records = 2000

# Generate incrementing ID column
data = {
    "ID": np.arange(1, num_records + 1),
    "DetailNumber": np.random.randint(1000, 9999, num_records),
    "LoadNumber": np.random.randint(1000, 9999, num_records),
    "LotNumber": np.random.randint(1000, 9999, num_records),
    "ShipmentLineID": np.random.randint(1000, 9999, num_records),
    "ReceiptKey": np.random.randint(1000, 9999, num_records),
    "ClientID": np.random.randint(100, 999, num_records),
    "WarehouseID": np.random.randint(10, 99, num_records),
    "SiteID": np.random.randint(10, 99, num_records),
    "ProductID": np.random.randint(1000, 9999, num_records),
    "InventoryStatusID": np.random.randint(10, 99, num_records),
    "StorageLocationID": np.random.randint(1000, 9999, num_records),
    "AssetTypeID": np.random.randint(1000, 9999, num_records),
    "HoldFlagBool": np.random.choice([0, 1], num_records),
    "UnitQTY": np.random.randint(1, 500, num_records),
    "Weight": np.random.random(num_records) * 1000,  # Weight in kg
    "Volume": np.random.random(num_records) * 10,  # Volume in cubic meters
    "Category": np.random.choice(["Electronics", "Clothing", "Furniture", "Food"], num_records),
    "Supplier": np.random.choice(["SupplierA", "SupplierB", "SupplierC"], num_records),
    "Status": np.random.choice(["Pending", "Shipped", "Delivered"], num_records),
    "Priority": np.random.choice(["High", "Medium", "Low"], num_records),
}

# Generate date columns
start_date = datetime(2020, 1, 1)
data["ManufacturedDateTime"] = [start_date + timedelta(days=int(np.random.randint(0, 1000))) for _ in range(num_records)]
data["ExpirationDateTime"] = [date + timedelta(days=int(np.random.randint(30, 365))) for date in data["ManufacturedDateTime"]]
data["ReceivedDateTime"] = [date + timedelta(days=int(np.random.randint(0, 30))) for date in data["ManufacturedDateTime"]]
data["AddedDateTime"] = [date + timedelta(days=int(np.random.randint(0, 10))) for date in data["ReceivedDateTime"]]
data["LastMoveDateTime"] = [date + timedelta(days=int(np.random.randint(0, 30))) for date in data["AddedDateTime"]]
data["Created"] = data["ManufacturedDateTime"]
data["Modified"] = [date + timedelta(days=int(np.random.randint(0, 100))) for date in data["Created"]]

# Convert to DataFrame
df = pd.DataFrame(data)

# Add random null values to columns
for col in df.columns:
    if col not in ["ID", "Created"]:
        null_rate = np.random.uniform(0.05, 0.3)  # 5% to 30% null values
        null_indices = np.random.choice(num_records, size=int(null_rate * num_records), replace=False)
        df.loc[null_indices, col] = np.nan

for col in df.columns:
    if df[col].dtype == int:
        df[col] = df[col].astype(float)

df.to_csv("synthetic_warehouse_data.csv", index=False)

print(df.head())
