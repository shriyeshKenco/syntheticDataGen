import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time

# Load the initial dataset
df = pd.read_csv("synthetic_logistics_data.csv", parse_dates=['Created', 'Modified'])

# Parameters
start_datetime = datetime(2024, 6, 10, 0, 0)
num_days = 10
active_hours = 16  # Active from 0800 to 2400 (inclusive)
inactive_hours = 8  # Inactive from 0000 to 0800
total_hours = active_hours + inactive_hours

# Estimate total number of records to be created based on means
total_estimated_creations = num_days * (
            np.random.normal(350, 65) * active_hours + np.random.normal(70, 20) * inactive_hours)
total_estimated_creations = int(total_estimated_creations * 1.5)  # Adding buffer

# Generate IDs for all new records
initial_max_id = df['ID'].max()
new_ids = np.arange(initial_max_id + 1, initial_max_id + 1 + total_estimated_creations)

# Index to keep track of the current ID
current_id_index = 0

# Configurations
CONFIG = {
    'DetailNumber': {'distribution': lambda num_records: np.random.randint(1000, 9999, num_records), 'null_rate': 0.1},
    'LoadNumber': {'distribution': lambda num_records: np.random.randint(1000, 9999, num_records), 'null_rate': 0.1},
    'LotNumber': {'distribution': lambda num_records: np.random.randint(1000, 9999, num_records), 'null_rate': 0.1},
    'ShipmentLineID': {'distribution': lambda num_records: np.random.randint(1000, 9999, num_records),
                       'null_rate': 0.1},
    'ReceiptKey': {'distribution': lambda num_records: np.random.randint(1000, 9999, num_records), 'null_rate': 0.1},
    'ClientID': {'distribution': lambda num_records: np.random.randint(100, 999, num_records), 'null_rate': 0.1},
    'WarehouseID': {'distribution': lambda num_records: np.random.randint(10, 99, num_records), 'null_rate': 0.1},
    'SiteID': {'distribution': lambda num_records: np.random.randint(10, 99, num_records), 'null_rate': 0.1},
    'ProductID': {'distribution': lambda num_records: np.random.randint(1000, 9999, num_records), 'null_rate': 0.1},
    'InventoryStatusID': {'distribution': lambda num_records: np.random.randint(10, 99, num_records), 'null_rate': 0.1},
    'StorageLocationID': {'distribution': lambda num_records: np.random.randint(1000, 9999, num_records),
                          'null_rate': 0.1},
    'AssetTypeID': {'distribution': lambda num_records: np.random.randint(1000, 9999, num_records), 'null_rate': 0.1},
    'HoldFlagBool': {'distribution': lambda num_records: np.random.choice([0, 1], num_records), 'null_rate': 0.1},
    'UnitQTY': {'distribution': lambda num_records: np.random.randint(1, 500, num_records), 'null_rate': 0.1},
    'Weight': {'distribution': lambda num_records: np.random.random(num_records) * 1000, 'null_rate': 0.05},
    'Volume': {'distribution': lambda num_records: np.random.random(num_records) * 10, 'null_rate': 0.05},
    'Category': {'distribution': lambda num_records: np.random.choice(["Electronics", "Clothing", "Furniture", "Food"],
                                                                      num_records, p=[0.7, 0.1, 0.1, 0.1]),
                 'null_rate': 0.1},
    'Supplier': {
        'distribution': lambda num_records: np.random.choice(["SupplierA", "SupplierB", "SupplierC"], num_records,
                                                             p=[0.5, 0.3, 0.2]), 'null_rate': 0.1},
    'Status': {'distribution': lambda num_records: np.random.choice(["Pending", "Shipped", "Delivered"], num_records),
               'null_rate': 0.1},
    'Priority': {'distribution': lambda num_records: np.random.choice(["High", "Medium", "Low"], num_records),
                 'null_rate': 0.1},
}


# Helper function to generate a timestamp within a specific hour
def random_timestamp_within_hour(base_date):
    minute = np.random.randint(0, 60)
    second = np.random.randint(0, 60)
    return base_date + timedelta(minutes=minute, seconds=second)


# Function to generate records
def create_records(num_records, current_datetime):
    global current_id_index
    new_records = {column: CONFIG[column]['distribution'](num_records) for column in CONFIG}
    new_records['ID'] = new_ids[current_id_index:current_id_index + num_records]
    current_id_index += num_records
    new_records['Created'] = [random_timestamp_within_hour(current_datetime) for _ in range(num_records)]
    new_records['Modified'] = new_records['Created']
    new_records['isDeleted'] = [False] * num_records
    new_records['Day'] = [current_datetime.date()] * num_records
    new_records['Hour'] = [current_datetime.hour] * num_records
    return pd.DataFrame(new_records)


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


# Start timing the entire process
start_time = time.time()

# Iterate through the days and hours
current_datetime = start_datetime
for day in range(num_days):
    day_start_time = time.time()

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
        new_records_df = create_records(num_creations, current_datetime)
        df = pd.concat([df, new_records_df], ignore_index=True)

        # Update records
        update_records(df, num_updates, current_datetime)

        # Delete records
        delete_records(df, num_deletes)

        # Move to the next hour
        current_datetime += timedelta(hours=1)

    day_end_time = time.time()
    print(f"Day {day + 1} processing time: {day_end_time - day_start_time:.2f} seconds")

# End timing the entire process
end_time = time.time()
print(f"Total processing time: {end_time - start_time:.2f} seconds")

# Save to CSV for later use
df.to_csv("synthetic_logistics_data_with_operations.csv", index=False)

# Display the first few rows of the DataFrame
print(df.head())
