import pandas as pd

# Read the order data
orders_df = pd.read_csv('order_data/order_data_2016-01-02', sep='\t')
orders_df.columns = ['order_id', 'driver_id', 'passenger_id', 'start_region_hash', 'dest_region_hash', 'price', 'time']

# Define a function to map date and time to slots
def map_to_slot(date_time):
    hour = date_time.hour
    minute = date_time.minute
    slot = hour if minute < 30 else hour + 1
    return slot % 24

# Convert 'time' column to datetime type
orders_df['time'] = pd.to_datetime(orders_df['time'])

# Map each date and time to a slot number
orders_df['slots'] = orders_df['time'].apply(map_to_slot)

# Convert the timestamp column to datetime objects
orders_df['time'] = pd.to_datetime(orders_df['time'])

# Map day of the week to numbers 1-7 (Monday-Sunday)
orders_df['day_of_week'] = orders_df['time'].dt.weekday + 1

# Group the data by start region and slots, and calculate the size
grouped_data_origin = orders_df.groupby('start_region_hash').size()

# Save the grouped data to a CSV file
grouped_data_origin.to_csv('regionSlotRequestsTotal.csv', header=['requests'], index_label='start_region_hash')
