import pandas as pd
import numpy as np
from windrose import WindroseAxes
import matplotlib.pyplot as plt
from matplotlib.colorbar import ColorbarBase
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
from persiantools.jdatetime import JalaliDateTime

# Load the data
file_path = "Filtered_PM2.5_Wind_Cleaned.csv"
data = pd.read_csv(file_path)

# Handle Persian datetime
def persian_to_gregorian(persian_datetime):
    return JalaliDateTime.strptime(persian_datetime, "%Y/%m/%d %H:%M:%S").to_gregorian()

def persian_season(date):
    """Determine the season based on the Persian calendar month."""
    month = date.month
    if month in [1, 2, 3]:  # Farvardin, Ordibehesht, Khordad
        return "Spring"
    elif month in [4, 5, 6]:  # Tir, Mordad, Shahrivar
        return "Summer"
    elif month in [7, 8, 9]:  # Mehr, Aban, Azar
        return "Autumn"
    else:  # Dey, Bahman, Esfand
        return "Winter"

# Convert Persian datetime to Gregorian for processing
data['datetime'] = data['datetime'].apply(persian_to_gregorian)
data['datetime'] = pd.to_datetime(data['datetime'])

# Convert back to Persian datetime for labeling
data['persian_datetime'] = data['datetime'].apply(JalaliDateTime.to_jalali)
data['Season'] = data['persian_datetime'].apply(lambda x: persian_season(x))
data['Year'] = data['persian_datetime'].apply(lambda x: x.year)

# Check for missing values
data.dropna(subset=['Wind speed', 'Wind angle', 'PM2.5 (m3/mg)'], inplace=True)

# Wind rose plotting function with PM overlay
def plot_wind_rose_with_PM(data, title, fixed_bins):
    """
    Plot a wind rose diagram with PM overlay. Adjust scatter size based on PM levels
    and use consistent wind speed bins across all plots.
    
    Parameters:
        data: DataFrame containing wind angle, wind speed, and PM levels.
        title: Title of the chart.
        fixed_bins: List of fixed bin edges for wind speed.
    """
    norm = Normalize(vmin=data['PM2.5 (m3/mg)'].min(), vmax=data['PM2.5 (m3/mg)'].max())
    cmap = plt.get_cmap("coolwarm")  # For PM levels
    rose_cmap = plt.get_cmap("jet")  # For wind speed bins, more contrast
    sm = ScalarMappable(cmap=cmap, norm=norm)

    # Create figure and wind rose axes
    fig, ax = plt.subplots(figsize=(12, 8), subplot_kw={'projection': 'windrose'})

    # Plot wind rose for wind speed with fixed bins
    ax.bar(
        data['Wind angle'],
        data['Wind speed'],
        normed=True,
        bins=fixed_bins,  # Use fixed bins for consistency
        opening=0.8,
        edgecolor='white',
        cmap=rose_cmap
    )

    # Overlay PM levels as scatter plot
    scatter_sizes = 25 + (data['PM2.5 (m3/mg)'] - data['PM2.5 (m3/mg)'].min()) / (data['PM2.5 (m3/mg)'].max() - data['PM2.5 (m3/mg)'].min()) * 90
    scatter = ax.scatter(
        data['Wind angle'],
        data['Wind speed'],
        c=data['PM2.5 (m3/mg)'],
        s=scatter_sizes,  # Size reflects PM levels
        cmap=cmap,
        alpha=0.7,
        edgecolor='black',
        norm=norm
    )

    ax.set_title(title, fontsize=14)

    # Add color bar for PM levels
    cbar_ax = fig.add_axes([0.9, 0.25, 0.02, 0.5])  # Adjust position for PM color bar
    cbar = ColorbarBase(cbar_ax, cmap=cmap, norm=norm, orientation='vertical')
    cbar.set_label('PM2.5 (m3/mg)', fontsize=12)

    # Adjust wind speed bin legend
    legend = ax.legend(
        bbox_to_anchor=(1.05, 0.5),  # Adjust closer to PM color bar
        loc='center left',
        fontsize=10,
        title="Wind Speed (m/s)"
    )
    legend.get_title().set_fontsize(11)

    # Adjust layout for cleaner view
    plt.subplots_adjust(left=0.1, right=0.85, top=0.85, bottom=0.15)
    plt.show()

# Define fixed bins for wind speed
fixed_bins = [0, 2, 4, 6, 8, 10, 12]  # Adjust as needed

# Seasonal wind roses
for season in data['Season'].unique():
    seasonal_data = data[data['Season'] == season]
    plot_wind_rose_with_PM(seasonal_data, f"Wind Rose for {season}", fixed_bins)

# Yearly wind roses
for year in data['Year'].unique():
    yearly_data = data[data['Year'] == year]
    plot_wind_rose_with_PM(yearly_data, f"Wind Rose for {year}", fixed_bins)