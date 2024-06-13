import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Load the initial dataset
df = pd.read_csv("synthetic_logistics_data.csv", parse_dates=['Created', 'Modified'])

# Parameters
start_datetime = datetime(2024, 6, 10, 0, 0)
num_days = 10
active_hours = 16  # Active from 0800 to 2400 (inclusive)
inactive_hours = 8  # Inactive from 0000 to 0800
total_hours = active_hours + inactive_hours


# Helper function to generate a timestamp within a specific hour
def random_timestamp_within_hour(base_date):
    minute = np.random.randint(0, 60)
    second = np.random.randint(0, 60)
    return base_date + timedelta(minutes=minute, seconds=second)


# Function to generate records
def create_records(num_records, start_id, current_datetime):
    new_records = []
    for i in range(num_records):
        new_record = {
            'ID': start_id + i,
            'DetailNumber': np.random.randint(1000, 9999),
            'LoadNumber': np.random.randint(1000, 9999),
            'LotNumber': np.random.randint(1000, 9999),
            'ShipmentLineID': np.random.randint(1000, 9999),
            'ReceiptKey': np.random.randint(1000, 9999),
            'ClientID': np.random.randint(100, 999),
            'WarehouseID': np.random.randint(10, 99),
            'SiteID': np.random.randint(10, 99),
            'ProductID': np.random.randint(1000, 9999),
            'InventoryStatusID': np.random.randint(10, 99),
            'StorageLocationID': np.random.randint(1000, 9999),
            'AssetTypeID': np.random.randint(1000, 9999),
            'HoldFlagBool': np.random.choice([0, 1]),
            'UnitQTY': np.random.randint(1, 500),
            'Weight': np.random.random() * 1000,
            'Volume': np.random.random() * 10,
            'Category': np.random.choice(["Electronics", "Clothing", "Furniture", "Food"], p=[0.7, 0.1, 0.1, 0.1]),
            'Supplier': np.random.choice(["SupplierA", "SupplierB", "SupplierC"], p=[0.5, 0.3, 0.2]),
            'Status': np.random.choice(["Pending", "Shipped", "Delivered"]),
            'Priority': np.random.choice(["High", "Medium", "Low"]),
            'ManufacturedDateTime': datetime(2020, 1, 1) + timedelta(days=int(np.random.randint(0, 1000))),
            'ExpirationDateTime': datetime(2020, 1, 1) + timedelta(days=int(np.random.randint(30, 365))),
            'ReceivedDateTime': datetime(2020, 1, 1) + timedelta(days=int(np.random.randint(0, 30))),
            'AddedDateTime': datetime(2020, 1, 1) + timedelta(days=int(np.random.randint(0, 10))),
            'LastMoveDateTime': datetime(2020, 1, 1) + timedelta(days=int(np.random.randint(0, 30))),
            'Created': random_timestamp_within_hour(current_datetime),
            'Modified': random_timestamp_within_hour(current_datetime),
            'isDeleted': False,
            'Day': current_datetime.date(),
            'Hour': current_datetime.hour
        }
        new_records.append(new_record)
    return new_records


# Function to update records
def update_records(df, num_updates, current_datetime):
    for _ in range(num_updates):
        # Select a random record that is not deleted
        candidates = df[df['isDeleted'] == False]
        if candidates.empty:
            break
        idx = np.random.choice(candidates.index)
        column_to_update = np.random.choice(['StorageLocationID', 'InventoryStatusID', 'Status', 'Priority'])
        new_value = np.random.randint(1000, 9999) if column_to_update == 'StorageLocationID' else np.random.choice(
            ["Pending", "Shipped", "Delivered", "High", "Medium", "Low"])
        df.loc[idx, column_to_update] = new_value
        df.loc[idx, 'Modified'] = random_timestamp_within_hour(current_datetime)


# Function to delete records
def delete_records(df, num_deletes):
    for _ in range(num_deletes):
        # Select a random record that is not deleted
        candidates = df[df['isDeleted'] == False]
        if candidates.empty:
            break
        idx = np.random.choice(candidates.index)
        df.loc[idx, 'isDeleted'] = True


# Iterate through the days and hours
current_datetime = start_datetime
next_id = df['ID'].max() + 1
for day in range(num_days):
    for hour in range(total_hours):
        if hour < inactive_hours:
            # Inactive hours
            num_creations = max(0, int(np.random.normal(70, 20)))
            num_updates = max(0, int(np.random.normal(30, 5)))
            num_deletes = max(0, int(np.random.normal(10, 5)))
        else:
            # Active hours
            num_creations = max(0, int(np.random.normal(350, 65)))
            num_updates = max(0, int(np.random.normal(80, 20)))
            num_deletes = max(0, int(np.random.normal(30, 15)))

        # Create records
        new_records = create_records(num_creations, next_id, current_datetime)
        new_records_df = pd.DataFrame(new_records)
        df = pd.concat([df, new_records_df], ignore_index=True)
        next_id += num_creations

        # Update records
        update_records(df, num_updates, current_datetime)

        # Delete records
        delete_records(df, num_deletes)

        # Move to the next hour
        current_datetime += timedelta(hours=1)

# Save to CSV for later use
df.to_csv("synthetic_logistics_data_with_operations.csv", index=False)

# Display the first few rows of the DataFrame
print(df.head())
