import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from sklearn.model_selection import KFold, cross_val_score
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns
from persiantools.jdatetime import JalaliDateTime
from scipy.stats import spearmanr
from scipy.stats import pearsonr


# Load the interpolated data
file_path = "Filtered_O3_Temperature_Interpolated.csv"
data = pd.read_csv(file_path)

# Convert Persian datetime to Gregorian datetime
def persian_to_gregorian(persian_datetime):
    return JalaliDateTime.strptime(persian_datetime, "%Y/%m/%d %H:%M:%S").to_gregorian()

# Apply conversion
data['datetime'] = data['datetime'].apply(persian_to_gregorian)
data['datetime'] = pd.to_datetime(data['datetime'])
data.set_index('datetime', inplace=True)

# Calculate Spearman correlation
correlation, p_value = spearmanr(data['O3 (ppb)'], data['Temperature'])

print(f"Spearman Correlation: {correlation}")
print(f"P-value: {p_value}")

# Interpretation
if p_value < 0.05:
    print("The Spearman correlation is statistically significant.")
else:
    print("The Spearman correlation is not statistically significant.")

# Calculate Pearson correlation
correlation, p_value = pearsonr(data['O3 (ppb)'], data['Temperature'])

print(f"Pearson Correlation: {correlation}")
print(f"P-value: {p_value}")

# Interpretation
if p_value < 0.05:
    print("The Pearson correlation is statistically significant.")
else:
    print("The Pearson correlation is not statistically significant.")

# Add lag features and rolling averages
data['O3_Lag1'] = data['O3 (ppb)'].shift(1)
data['O3_Lag2'] = data['O3 (ppb)'].shift(2)
data['O3_Lag3'] = data['O3 (ppb)'].shift(3)
data['Temp_Lag1'] = data['Temperature'].shift(1)
data['Temp_Lag2'] = data['Temperature'].shift(2)
data['Temp_Lag3'] = data['Temperature'].shift(3)
data['O3_RollingMean'] = data['O3 (ppb)'].rolling(window=3).mean()
data['Temp_RollingMean'] = data['Temperature'].rolling(window=3).mean()

# Extract time-based features
data['hour'] = data.index.hour
data['day_of_week'] = data.index.dayofweek
data['month'] = data.index.month
data['year'] = data.index.year

# Drop rows with missing values
data.dropna(inplace=True)

# Features and target variable
X = data[['Temperature', 'O3_Lag1', 'O3_Lag2', 'O3_Lag3', 'Temp_Lag1', 'Temp_Lag2', 'Temp_Lag3',
          'O3_RollingMean', 'Temp_RollingMean', 'hour', 'day_of_week', 'month', 'year']]
y = data['O3 (ppb)']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=None, shuffle=False)

# Train XGBoost Regressor
xgb_model = XGBRegressor(
    objective='reg:squarederror',
    n_estimators=150,
    learning_rate=0.1,
    max_depth=4,
    subsample=0.8,
    colsample_bytree=1,
    random_state=None,
    gamma=0
)
# Define 5-fold cross-validation
kfold = KFold(n_splits=5, shuffle=True, random_state=42)  # shuffle=True for randomness
xgb_model.fit(X_train, y_train)

# Perform cross-validation
mse_scores = -cross_val_score(xgb_model, X, y, cv=kfold, scoring='neg_mean_squared_error')
r2_scores = cross_val_score(xgb_model, X, y, cv=kfold, scoring='r2')

# Print the results
print(f"5-Fold Cross-Validation MSE: {np.mean(mse_scores):.4f} (±{np.std(mse_scores):.4f})")
print(f"5-Fold Cross-Validation R²: {np.mean(r2_scores):.4f} (±{np.std(r2_scores):.4f})")

# Feature Importance Plot
feature_importances = xgb_model.feature_importances_
plt.figure(figsize=(12, 6))
plt.barh(X.columns, feature_importances, color='darkgreen')
plt.title("Feature Importance")
plt.xlabel("Importance")
plt.ylabel("Feature")
plt.grid()
plt.show()

# Visualization of Hourly Changes
plt.figure(figsize=(14, 8))
sns.lineplot(x=data['hour'], y=data['O3 (ppb)'], ci=None, label='O3 (ppb)', color='blue')
sns.lineplot(x=data['hour'], y=data['Temperature'], ci=None, label='Temperature', color='orange')
plt.title("Hourly Changes in O3 Levels and Temperature")
plt.xlabel("Hour of Day")
plt.ylabel("Value")
plt.legend()
plt.grid()
plt.show()

# Scatter Plot of Ozone vs Temperature
plt.figure(figsize=(12, 6))
sns.scatterplot(x=data['Temperature'], y=data['O3 (ppb)'], alpha=0.5)
plt.title("Scatter Plot: Ozone Levels vs Temperature")
plt.xlabel("Temperature")
plt.ylabel("O3 (ppb)")
plt.grid()
plt.show()

# Plot actual vs predicted values
plt.figure(figsize=(20, 6))
plt.plot(y_test.values, label='Actual O3 (ppb)', color='red')
plt.plot(y_pred, label='Predicted O3 (ppb)', color='darkgreen', linestyle='--')
plt.legend()
plt.title('Actual vs Predicted O3 Levels')
plt.xlabel('Time')
plt.ylabel('O3 (ppb)')
plt.show()