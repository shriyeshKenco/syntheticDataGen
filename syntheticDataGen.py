import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Set random seed for reproducibility
np.random.seed(42)

# Number of records
num_records = 2000
max_date = datetime(2024, 6, 10, 12, 0)  # Maximum allowed date/time

# Helper function to generate random times during peak working hours
def generate_working_hour_timestamps(base_date, num_records):
    timestamps = []
    for _ in range(num_records):
        random_seconds = int(np.random.lognormal(mean=10, sigma=1))
        # Ensure the time falls within 09:00 to 17:00
        while True:
            time_of_day = timedelta(seconds=random_seconds % (8 * 3600)) + timedelta(hours=9)
            if timedelta(hours=9) <= time_of_day <= timedelta(hours=17):
                break
            random_seconds = int(np.random.lognormal(mean=10, sigma=1))
        timestamps.append(base_date + timedelta(seconds=random_seconds))
    return timestamps

# Configuration specification for each column
CONFIG = {
    'ID': {
        'distribution': lambda num_records: np.arange(1, num_records + 1),
        'null_rate': 0.0
    },
    'DetailNumber': {
        'distribution': lambda num_records: np.random.randint(1000, 9999, num_records),
        'null_rate': 0.1
    },
    'LoadNumber': {
        'distribution': lambda num_records: np.random.randint(1000, 9999, num_records),
        'null_rate': 0.1
    },
    'LotNumber': {
        'distribution': lambda num_records: np.random.randint(1000, 9999, num_records),
        'null_rate': 0.1
    },
    'ShipmentLineID': {
        'distribution': lambda num_records: np.random.randint(1000, 9999, num_records),
        'null_rate': 0.1
    },
    'ReceiptKey': {
        'distribution': lambda num_records: np.random.randint(1000, 9999, num_records),
        'null_rate': 0.1
    },
    'ClientID': {
        'distribution': lambda num_records: np.random.randint(100, 999, num_records),
        'null_rate': 0.1
    },
    'WarehouseID': {
        'distribution': lambda num_records: np.random.randint(10, 99, num_records),
        'null_rate': 0.1
    },
    'SiteID': {
        'distribution': lambda num_records: np.random.randint(10, 99, num_records),
        'null_rate': 0.1
    },
    'ProductID': {
        'distribution': lambda num_records: np.random.randint(1000, 9999, num_records),
        'null_rate': 0.1
    },
    'InventoryStatusID': {
        'distribution': lambda num_records: np.random.randint(10, 99, num_records),
        'null_rate': 0.1
    },
    'StorageLocationID': {
        'distribution': lambda num_records: np.random.randint(1000, 9999, num_records),
        'null_rate': 0.1
    },
    'AssetTypeID': {
        'distribution': lambda num_records: np.random.randint(1000, 9999, num_records),
        'null_rate': 0.1
    },
    'HoldFlagBool': {
        'distribution': lambda num_records: np.random.choice([0, 1], num_records),
        'null_rate': 0.1
    },
    'UnitQTY': {
        'distribution': lambda num_records: np.random.randint(1, 500, num_records),
        'null_rate': 0.1
    },
    'Weight': {
        'distribution': lambda num_records: np.random.random(num_records) * 1000,
        'null_rate': 0.05
    },
    'Volume': {
        'distribution': lambda num_records: np.random.random(num_records) * 10,
        'null_rate': 0.05
    },
    'Category': {
        'distribution': lambda num_records: np.random.choice(["Electronics", "Clothing", "Furniture", "Food"], num_records, p=[0.7, 0.1, 0.1, 0.1]),
        'null_rate': 0.1
    },
    'Supplier': {
        'distribution': lambda num_records: np.random.choice(["SupplierA", "SupplierB", "SupplierC"], num_records, p=[0.5, 0.3, 0.2]),
        'null_rate': 0.1
    },
    'Status': {
        'distribution': lambda num_records: np.random.choice(["Pending", "Shipped", "Delivered"], num_records),
        'null_rate': 0.1
    },
    'Priority': {
        'distribution': lambda num_records: np.random.choice(["High", "Medium", "Low"], num_records),
        'null_rate': 0.1
    },
    # Date columns
    'ManufacturedDateTime': {
        'distribution': lambda num_records: [datetime(2020, 1, 1) + timedelta(days=int(np.random.randint(0, 1000))) for _ in range(num_records)],
        'null_rate': 0.0
    },
    'ExpirationDateTime': {
        'distribution': lambda num_records: [date + timedelta(days=int(np.random.randint(30, 365))) for date in CONFIG['ManufacturedDateTime']['distribution'](num_records)],
        'null_rate': 0.0
    },
    'ReceivedDateTime': {
        'distribution': lambda num_records: [date + timedelta(days=int(np.random.randint(0, 30))) for date in CONFIG['ManufacturedDateTime']['distribution'](num_records)],
        'null_rate': 0.0
    },
    'AddedDateTime': {
        'distribution': lambda num_records: [date + timedelta(days=int(np.random.randint(0, 10))) for date in CONFIG['ReceivedDateTime']['distribution'](num_records)],
        'null_rate': 0.0
    },
    'LastMoveDateTime': {
        'distribution': lambda num_records: [date + timedelta(days=int(np.random.randint(0, 30))) for date in CONFIG['AddedDateTime']['distribution'](num_records)],
        'null_rate': 0.0
    },
    'Created': {
        'distribution': lambda num_records: generate_working_hour_timestamps(datetime(2020, 1, 1), num_records),
        'null_rate': 0.0
    },
    'Modified': {
        'distribution': lambda num_records: [],
        'null_rate': 0.0
    },
    'isDeleted': {
        'distribution': lambda num_records: [False] * num_records,
        'null_rate': 0.0
    }
}

# Generate data using the configuration
data = {key: CONFIG[key]['distribution'](num_records) for key in CONFIG if key != 'Modified'}

# Ensure Created <= LastMoveDateTime <= Modified
data['Modified'] = [
    created + timedelta(seconds=int(np.random.randint(0, (max_date - created).total_seconds())))
    for created in data['Created']
]

# Ensure LastMoveDateTime <= Modified
data['LastMoveDateTime'] = [
    min(last_move, modified) for last_move, modified in zip(data['LastMoveDateTime'], data['Modified'])
]

# Ensure Created <= LastMoveDateTime
data['Created'] = [
    min(created, last_move) for created, last_move in zip(data['Created'], data['LastMoveDateTime'])
]

# Convert to DataFrame
df = pd.DataFrame(data)

# Add random null values to columns based on specified null rates
for col in df.columns:
    null_rate = CONFIG[col]['null_rate']
    if null_rate > 0:
        null_indices = np.random.choice(num_records, size=int(null_rate * num_records), replace=False)
        df.loc[null_indices, col] = np.nan

# Convert integer columns with NaNs to float
for col in df.columns:
    if df[col].dtype == np.int64:
        df[col] = df[col].astype(float)

# Save to CSV for later use
df.to_csv("synthetic_logistics_data.csv", index=False)

# Display the first few rows of the DataFrame
print(df.head())
