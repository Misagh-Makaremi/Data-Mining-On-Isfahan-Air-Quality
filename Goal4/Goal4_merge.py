import pandas as pd
from persiantools.jdatetime import JalaliDateTime

# Load the datasets
total_data = pd.read_csv("Total_Data_Cleaned.csv")
filtered_data = pd.read_csv("Filtered_O3_Wind_Cleaned.csv")

# Ensure datetime columns are converted to Persian datetime
def persian_to_gregorian(persian_datetime):
    return JalaliDateTime.strptime(persian_datetime, "%Y/%m/%d %H:%M:%S").to_gregorian()

# Convert Persian datetime to Gregorian datetime for both datasets
total_data['datetime'] = total_data['datetime'].apply(persian_to_gregorian)
filtered_data['datetime'] = filtered_data['datetime'].apply(persian_to_gregorian)

# Set datetime as index for both datasets
total_data['datetime'] = pd.to_datetime(total_data['datetime'])
filtered_data['datetime'] = pd.to_datetime(filtered_data['datetime'])

total_data.set_index('datetime', inplace=True)
filtered_data.set_index('datetime', inplace=True)

# Group by datetime and compute the mean PM2.5 values across stations
pm25_mean = total_data.groupby('datetime')['PM2.5 (m3/mg)'].mean()

# Merge the PM2.5 mean column into the filtered_data
filtered_data['PM2.5 (m3/mg)'] = pm25_mean

# Interpolate missing PM2.5_mean values (ensure the index is a DatetimeIndex)
filtered_data['PM2.5 (m3/mg)'] = filtered_data['PM2.5 (m3/mg)'].interpolate(method='time')

# Drop the O3 (ppb) column
filtered_data.drop(columns=['O3 (ppb)'], inplace=True)

# Convert Gregorian datetime index back to Persian datetime
def gregorian_to_persian(gregorian_datetime):
    return JalaliDateTime.to_jalali(gregorian_datetime).strftime("%Y/%m/%d %H:%M:%S")

filtered_data.reset_index(inplace=True)  # Temporarily reset index for conversion
filtered_data['datetime'] = filtered_data['datetime'].apply(gregorian_to_persian)
filtered_data.set_index('datetime', inplace=True)  # Set back to Persian datetime index

# Save the final data to a new CSV file
filtered_data.to_csv("Filtered_PM2.5_Wind_Cleaned.csv")

print("File saved as 'Filtered_PM2.5_Wind_Cleaned.csv'.")
