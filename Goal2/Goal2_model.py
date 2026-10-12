import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
from xgboost import XGBRegressor
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import spearmanr
from scipy.stats import pearsonr

# Load the data
filtered_file = "Filtered_O3_Wind_Cleaned.csv"

data = pd.read_csv(filtered_file)

# Drop rows with missing values (if any remain)
data.dropna(inplace=True)

# Standardize numerical features (Wind speed, Wind angle)
scaler = StandardScaler()
scaled_features = scaler.fit_transform(data[['Wind speed', 'Wind angle']])
data[['Wind speed', 'Wind angle']] = scaled_features

# Define features (predictors) and target (response)
X = data[['Wind speed', 'Wind angle']]
y = data['O3 (ppb)']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the XGBoost model
xgb_model = XGBRegressor(objective='reg:squarederror', n_estimators=100, learning_rate=0.1, max_depth=5, random_state=42)
xgb_model.fit(X_train, y_train)

# Predictions and evaluation
y_pred = xgb_model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error: {mse}")
print(f"R-squared: {r2}")

# Feature importance
importances = xgb_model.feature_importances_
plt.figure(figsize=(8, 6))
plt.bar(X.columns, importances, color='skyblue')
plt.title("Feature Importance")
plt.ylabel("Importance Score")
plt.xlabel("Feature")
plt.show()

# Partial Dependence Plots
from sklearn.inspection import PartialDependenceDisplay

fig, ax = plt.subplots(figsize=(12, 6))
PartialDependenceDisplay.from_estimator(xgb_model, X_train, [0, 1], feature_names=['Wind speed', 'Wind angle'], ax=ax)
plt.suptitle("Partial Dependence Plots for Wind Speed and Wind Angle", fontsize=16)
plt.show()

# Scatter Plot: Predicted vs. Actual Ozone Levels
plt.figure(figsize=(10, 6))
plt.scatter(y_test, y_pred, alpha=0.6, color='blue')
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], color='red', linestyle='--', linewidth=2)
plt.title("Predicted vs. Actual Ozone Levels")
plt.xlabel("Actual O3 (ppb)")
plt.ylabel("Predicted O3 (ppb)")
plt.grid()
plt.show()


# Calculate Spearman correlation
correlation, p_value = spearmanr(data['O3 (ppb)'], data['Wind speed'])

print(f"Spearman Correlation: {correlation}")
print(f"P-value: {p_value}")

# Interpretation
if p_value < 0.05:
    print("The Spearman correlation is statistically significant.")
else:
    print("The Spearman correlation is not statistically significant.")

# Calculate Pearson correlation
correlation, p_value = pearsonr(data['O3 (ppb)'], data['Wind speed'])

print(f"Pearson Correlation: {correlation}")
print(f"P-value: {p_value}")

# Interpretation
if p_value < 0.05:
    print("The Pearson correlation is statistically significant.")
else:
    print("The Pearson correlation is not statistically significant.")