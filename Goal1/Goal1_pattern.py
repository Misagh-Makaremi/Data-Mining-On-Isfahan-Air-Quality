import pandas as pd
from persiantools.jdatetime import JalaliDateTime
from statsmodels.tsa.seasonal import seasonal_decompose
import matplotlib.pyplot as plt
import seaborn as sns

# Load the cleaned data
file_path = "Filtered_O3_Temperature_Interpolated.csv"
data = pd.read_csv(file_path)

# Convert Persian datetime to Gregorian for processing
def persian_to_gregorian(persian_datetime):
    return JalaliDateTime.strptime(persian_datetime, "%Y/%m/%d %H:%M:%S").to_gregorian()

# Apply conversion
data['datetime'] = data['datetime'].apply(persian_to_gregorian)

# Convert to pandas datetime format
data['datetime'] = pd.to_datetime(data['datetime'])

# Set datetime as index for time-series decomposition
data.set_index('datetime', inplace=True)

# Step 1: Time-Series Decomposition
# Set the default color cycle to dark green
plt.rcParams['axes.prop_cycle'] = plt.cycler(color=['darkgreen'])
result = seasonal_decompose(data['O3 (ppb)'], model='additive', period=24 * 365)  # Daily periodicity
result.plot()
plt.gcf().set_size_inches(15, 10)  # Larger plot size
plt.suptitle("Time-Series Decomposition of O3 (ppb)", fontsize=16)
plt.show()

# Convert back to Persian datetime for visualization
data['persian_datetime'] = data.index.to_series().apply(lambda x: JalaliDateTime.to_jalali(x))

# Step 2: Visualization of Changes

# Add hour, month, and year columns for grouping
data['hour'] = data.index.hour
data['month'] = data.index.month
data['year'] = data.index.year

# Hourly changes
plt.figure(figsize=(12, 6))
sns.lineplot(x='hour', y='O3 (ppb)', data=data, ci=None, label="Hourly O3 Levels")
sns.lineplot(x='hour', y='Temperature', data=data, ci=None, label="Hourly Temperature")
plt.title("Hourly Changes in O3 Levels and Temperature", fontsize=14)
plt.xlabel("Hour of Day")
plt.ylabel("Value")
plt.legend()
plt.grid()
plt.show()

# Monthly changes
plt.figure(figsize=(12, 6))
sns.boxplot(x='month', y='O3 (ppb)', data=data)
plt.title("Monthly Changes in O3 Levels", fontsize=14)
plt.xlabel("Month")
plt.ylabel("O3 (ppb)")
plt.grid()
plt.show()

##################
# Exclude non-numeric columns for aggregation
numeric_data = data.select_dtypes(include=['number'])

# Add month and year columns for grouping
data['month'] = data.index.month
data['year'] = data.index.year

# Monthly averages for seasonal changes
monthly_avg = numeric_data.groupby(data['month']).mean()

# Plot Seasonal (Monthly Average) Changes
plt.figure(figsize=(12, 6))
sns.lineplot(data=monthly_avg[['O3 (ppb)', 'Temperature']])
plt.title("Seasonal (Monthly Average) O3 Levels and Temperature", fontsize=14)
plt.xlabel("Month")
plt.ylabel("Average Value")
plt.legend(['O3 (ppb)', 'Temperature'])
plt.grid()
plt.show()

##################

# Yearly changes
plt.figure(figsize=(12, 6))
sns.boxplot(x='year', y='O3 (ppb)', data=data)
plt.title("Yearly Changes in O3 Levels", fontsize=14)
plt.xlabel("Year")
plt.ylabel("O3 (ppb)")
plt.grid()
plt.show()