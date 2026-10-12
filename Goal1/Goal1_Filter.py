import pandas as pd

# Load the cleaned dataset
file_path = "Total_Data_Cleaned.csv"
data = pd.read_csv(file_path)

# Step 1: Filter relevant stations and columns
filtered_data = data[data['Station'].isin(['Shahr Isfahan', '25 Aban'])]
filtered_data = filtered_data[['datetime', 'Station', 'O3 (ppb)', 'Temperature']]

# Step 2: Pivot data to have separate columns for each station's O3 and Temperature
pivoted_data = filtered_data.pivot_table(
    index='datetime',
    columns='Station',
    values=['O3 (ppb)', 'Temperature']
).reset_index()

# Flatten multi-level column names
pivoted_data.columns = ['datetime', 'O3_SI', 'O3_25A', 'Temp_SI', 'Temp_25A']

# Step 3: Combine O3 (ppb) data into a single column
pivoted_data['O3 (ppb)'] = pivoted_data[['O3_SI', 'O3_25A']].mean(axis=1, skipna=True)

# Step 4: Combine Temperature data into a single column (optional, if you want one column for Temperature)
pivoted_data['Temperature'] = pivoted_data[['Temp_SI', 'Temp_25A']].mean(axis=1, skipna=True)

# Step 5: Keep only datetime, O3 (ppb), and Temperature columns
final_data = pivoted_data[['datetime', 'O3 (ppb)', 'Temperature']]

# Save the result to a new CSV file
output_path = "Filtered_O3_Temperature.csv"
final_data.to_csv(output_path, index=False)

print("Filtered and combined data saved to:", output_path)
