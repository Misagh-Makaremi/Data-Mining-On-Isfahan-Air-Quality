# Data-Mining-On-Isfahan-Air-Quality
## Statistical analysis and data mining over 6 years of Isfahan air quality data
<img width="794" height="400" alt="image" src="https://github.com/user-attachments/assets/17885516-5849-4584-8648-41778c79e7b0" />

### Introduction
The present project was carried out using 6 years of air quality data in Isfahan. The data was provided by the Transportation and Traffic Department of Isfahan Municipality, which included two data sets: “pollutant concentrations” and “meteorological indices”.
The first set belongs to 13 active air quality monitoring stations in Isfahan city, the names and locations of which can be seen in the file. The second set is related to the meteorological data of the Isfahan airport station, which monitors weather indices.
In the following, we try to examine the four key focuses of this project by using appropriate methods:
1. Investigating the pattern of hourly changes in ozone pollutants, proportional to temperature and radiation changes over a 6-year period.
2. Investigating ozone changes proportional to wind patterns in Isfahan city over a 6-year period.
3. Investigating the effect of nitrogen oxide concentrations on increasing and decreasing ozone concentrations.
4. Investigating 6-year changes in particulate matter pollutants and its relationship with meteorological data (wind speed and direction).

### Getting familiar with datasets
🗃️This dataset includes two files related to the climate and pollutant data of Isfahan. The excel file named METAR actually contains meteorological data, and the excel file named Quality contains data related to the concentration of various pollutants. This data is in the form of a time series and covers the period from the beginning of 1397 to the end of 1402 SH. The data was also recorded hourly and daily during this period. It should be noted that 13 air quality monitoring stations are currently active, and only 1 station "25 Aban" is equipped with an ozone analyzer. Also, all 13 stations measure PM2.5 pollutants.
#### What's in here? *(Let's explain features)*
##### 😷Air Quality Features:
- CO (Carbon Monoxide) [ppm]
- O₃ (Ozone) [ppb]
- NO (Nitric Oxide) [ppb]
- NO₂ (Nitrogen Dioxide) [ppb]
- NOx (Nitrogen Oxides) [ppb]
- SO₂ (Sulfur Dioxide) [ppb]
- PM10 (Particulate Matter ≤10 µm) [µg/m³]
- PM2.5 (Particulate Matter ≤2.5 µm) [µg/m³]
##### 🌡️Meteorological Features:
- Wind Speed [m/s]
- Wind Angle/Direction [Degrees]
- Temperature [°C]
- Relative Humidity [%]
- Dew Point Temperature [°C]
- Pressure [hPa]
- Visibility [km]
- Clouds [Octas]
#### 📝License
This data was provided to interested parties by the Transportation and Traffic Department of Isfahan Municipality for the purpose of participating in a statistical analysis competition. As a result, the material and intellectual rights of this dataset are in the possession of Isfahan Municipality.
