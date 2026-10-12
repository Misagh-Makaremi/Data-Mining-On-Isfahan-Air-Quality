import pandas as pd

# Load the dataset
data = pd.read_csv("Filtered_O3_Wind.csv")

# Handle missing values
# Forward fill followed by backward fill
data.fillna(method='ffill', inplace=True)
data.fillna(method='bfill', inplace=True)

# Check for any remaining missing values
if data.isnull().sum().sum() == 0:
    print("All missing values have been successfully handled.")
else:
    print("Some missing values still remain in the dataset.")

# Save the cleaned dataset (optional)
data.to_csv("Filtered_O3_Wind_Cleaned.csv", index=False)

# Now proceed with the linear regression or any other analysis
