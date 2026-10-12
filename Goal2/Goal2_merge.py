import pandas as pd
from persiantools.jdatetime import JalaliDateTime

# Load the datasets
filtered_data = pd.read_csv("Filtered_O3_Temperature_Interpolated.csv")
total_data = pd.read_csv("Total_Data_Cleaned.csv")

# Function to convert Persian datetime to Gregorian
def persian_to_gregorian(persian_datetime):
    return JalaliDateTime.strptime(persian_datetime, "%Y/%m/%d %H:%M:%S").to_gregorian()

# Convert Persian datetime in both datasets to Gregorian
filtered_data['datetime'] = filtered_data['datetime'].apply(persian_to_gregorian)
filtered_data['datetime'] = pd.to_datetime(filtered_data['datetime'])

total_data['datetime'] = total_data['datetime'].apply(persian_to_gregorian)
total_data['datetime'] = pd.to_datetime(total_data['datetime'])

# Filter total_data for the required stations
filtered_stations = total_data[total_data['Station'].isin(['Shahr Isfahan', '25 Aban'])]

# Select relevant columns: datetime and wind-related features
wind_data = filtered_stations[['datetime', 'Wind speed', 'Wind angle', 'Wind direction']]

# Drop duplicates to ensure unique datetime entries
# Since the values of the two stations are the same, dropping duplicates is safe
wind_data = wind_data.drop_duplicates(subset='datetime')

# Merge wind data with filtered O3 data
merged_data = pd.merge(filtered_data, wind_data, on='datetime', how='left')

# Drop the Temperature column as per your requirement
merged_data.drop(columns=['Temperature'], inplace=True)

# Convert datetime back to Persian format
merged_data['datetime'] = merged_data['datetime'].apply(lambda x: JalaliDateTime.to_jalali(x).strftime('%Y/%m/%d %H:%M:%S'))

# Save the resulting dataset
merged_data.to_csv("Filtered_O3_Wind.csv", index=False)

print("Data merged successfully and saved to 'Filtered_O3_Wind.csv'.")
