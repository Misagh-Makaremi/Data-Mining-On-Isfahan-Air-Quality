import pandas as pd

# Load the datasets
metar_df = pd.read_excel("METAR.xlsx")
quality_df = pd.read_excel("Quality.xlsx")

import jdatetime

# Convert Persian date to Gregorian and combine with time
def persian_to_gregorian(row):
    persian_date = jdatetime.date(*map(int, row["Date"].split("/")))  # Split Persian date into components
    gregorian_date = persian_date.togregorian()  # Convert to Gregorian
    return f"{gregorian_date} {row['Time']}"

# Apply conversion for both datasets
metar_df["datetime"] = pd.to_datetime(
    metar_df.apply(persian_to_gregorian, axis=1)
)
quality_df["datetime"] = pd.to_datetime(
    quality_df.apply(persian_to_gregorian, axis=1)
)

# Proceed with the merge and cleanup
metar_df.drop(columns=["Station", "Date", "Time"], inplace=True)
quality_df.drop(columns=["Date", "Time"], inplace=True)

merged_df = pd.merge(quality_df, metar_df, on="datetime", how="outer")
merged_df = merged_df.sort_values(by="datetime").reset_index(drop=True)

# Save to file if needed
merged_df.to_csv("merged_data.csv", index=False)


from jdatetime import date

# Add Persian date
merged_df["persian_date"] = merged_df["datetime"].apply(
    lambda x: date.fromgregorian(date=x.date()).strftime("%Y-%m-%d")
)

# Sort by Persian date
merged_df.sort_values(by=["persian_date", "datetime"], inplace=True)

# Load the merged data
merged_df = pd.read_csv("merged_data.csv")

# Convert datetime column to Persian calendar
def to_persian_calendar(gregorian_datetime):
    # Split date and time
    date_part, time_part = gregorian_datetime.split(" ")
    # Convert Gregorian date to Persian
    gregorian_date = pd.to_datetime(date_part)
    persian_date = jdatetime.date.fromgregorian(date=gregorian_date).strftime("%Y/%m/%d")
    # Combine Persian date with time
    return f"{persian_date} {time_part}"

merged_df["datetime"] = merged_df["datetime"].apply(to_persian_calendar)

# Save the updated data
merged_df.to_csv("Total_Data.csv", index=False)
