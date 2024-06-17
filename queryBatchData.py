import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time

# Load the initial dataset
df = pd.read_csv("synthetic_logistics_data.csv", parse_dates=['Created', 'Modified'])

# Ensure Day and Hour columns are added to the dataframe
if 'Day' not in df.columns:
    df['Day'] = pd.NaT
if 'Hour' not in df.columns:
    df['Hour'] = pd.NaT

# Parameters
start_datetime = datetime(2024, 6, 10, 6, 0)  # Starting at 06:00 on June 10th, 2024
num_days = 1
active_hours = 16  # Active from 0600 to 2200 (inclusive)
inactive_hours = 8  # Inactive from 2200 to 0600
total_hours = active_hours + inactive_hours

# Estimate total number of records to be created based on means
total_estimated_creations = num_days * (
            np.random.normal(350, 65) * active_hours + np.random.normal(70, 20) * inactive_hours)
total_estimated_creations = int(total_estimated_creations * 1.5)  # Adding buffer

# Start IDs from 2001
new_ids = np.arange(2001, 2001 + total_estimated_creations)

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
    new_records['Day'] = [current_datetime.strftime('%Y-%m-%d')] * num_records  # Populate the Day column
    new_records['Hour'] = [current_datetime.hour] * num_records  # Populate the Hour column
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
        df.loc[idx, 'Day'] = current_datetime.strftime('%Y-%m-%d')  # Update the Day column
        df.loc[idx, 'Hour'] = current_datetime.hour  # Update the Hour column


# Function to delete records
def delete_records(df, num_deletes, current_datetime):
    for _ in range(num_deletes):
        # Select a random record that is not deleted
        candidates = df[df['isDeleted'] == False]
        if candidates.empty:
            break
        idx = np.random.choice(candidates.index)
        df.loc[idx, 'isDeleted'] = True
        df.loc[idx, 'Modified'] = random_timestamp_within_hour(current_datetime)
        df.loc[idx, 'Day'] = current_datetime.strftime('%Y-%m-%d')  # Update the Day column
        df.loc[idx, 'Hour'] = current_datetime.hour  # Update the Hour column


# Start timing the entire process
start_time = time.time()

# Iterate through the days and hours
current_datetime = start_datetime
for day in range(num_days):
    day_start_time = time.time()

    for hour in range(total_hours):
        if hour < active_hours:
            # Active hours
            num_creations = max(0, int(np.random.normal(350, 65)))
            num_updates = max(0, int(np.random.normal(80, 20)))
            num_deletes = max(0, int(np.random.normal(30, 15)))
        else:
            # Inactive hours
            num_creations = max(0, int(np.random.normal(70, 20)))
            num_updates = max(0, int(np.random.normal(30, 5)))
            num_deletes = max(0, int(np.random.normal(10, 5)))

        # Create records
        new_records_df = create_records(num_creations, current_datetime)
        df = pd.concat([df, new_records_df], ignore_index=True)

        # Update records
        update_records(df, num_updates, current_datetime)

        # Delete records
        delete_records(df, num_deletes, current_datetime)

        # Move to the next hour
        current_datetime += timedelta(hours=1)

        # Check if the time is outside the active hours (22:00 - 06:00)
        if current_datetime.hour >= 22 or current_datetime.hour < 6:
            current_datetime += timedelta(hours=(24 - current_datetime.hour + 6))  # Skip to next active hour at 06:00

    day_end_time = time.time()
    print(f"Day {day + 1} processing time: {day_end_time - day_start_time:.2f} seconds")

# End timing the entire process
end_time = time.time()
print(f"Total processing time: {end_time - start_time:.2f} seconds")

# Save to CSV for later use
df.to_csv("synthetic_logistics_data_with_operations.csv", index=False)

# Display the first few rows of the DataFrame
print(df.head())
