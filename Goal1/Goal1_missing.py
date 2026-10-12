import pandas as pd
from persiantools.jdatetime import JalaliDateTime

# Load the filtered data
file_path = "Filtered_O3_Temperature.csv"
data = pd.read_csv(file_path)

# Step 1: Convert datetime to Gregorian for processing
# Create a helper function to convert Persian to Gregorian
def persian_to_gregorian(persian_datetime):
    return JalaliDateTime.strptime(persian_datetime, "%Y/%m/%d %H:%M:%S").to_gregorian()

# Apply conversion
data['datetime'] = data['datetime'].apply(persian_to_gregorian)

# Step 2: Set datetime as the index
data['datetime'] = pd.to_datetime(data['datetime'])  # Ensure proper datetime format
data.set_index('datetime', inplace=True)

# Step 3: Perform time-based interpolation
data[['O3 (ppb)', 'Temperature']] = data[['O3 (ppb)', 'Temperature']].interpolate(
    method="time", limit_direction="both"
)

# Step 4: (Optional) Convert datetime back to Persian format
# Reset the index to include datetime as a column
data.reset_index(inplace=True)

# Convert datetime back to Persian format
data['datetime'] = data['datetime'].apply(lambda dt: JalaliDateTime.to_jalali(dt).strftime("%Y/%m/%d %H:%M:%S"))

# Save the result to a new CSV file
output_path = "Filtered_O3_Temperature_Interpolated.csv"
data.to_csv(output_path, index=False)

print("Interpolated data saved to:", output_path)
