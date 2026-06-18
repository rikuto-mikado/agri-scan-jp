import openmeteo_requests

import pandas as pd
import requests_cache
from retry_requests import retry

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": 35.41,
    "longitude": 139.41,
    "daily": [
        "temperature_2m_max",
        "temperature_2m_min",
        "precipitation_sum",
        "sunshine_duration",
        "shortwave_radiation_sum",
        "wind_speed_10m_max",
        "wind_gusts_10m_max",
    ],
    "hourly": [
        "soil_temperature_0cm",
        "soil_temperature_6cm",
        "soil_temperature_18cm",
        "soil_moisture_0_to_1cm",
        "soil_moisture_1_to_3cm",
        "soil_moisture_3_to_9cm",
        "soil_moisture_9_to_27cm",
        "et0_fao_evapotranspiration",
        "vapour_pressure_deficit",
        "shortwave_radiation",
        "sunshine_duration",
        "wet_bulb_temperature_2m",
        "global_tilted_irradiance",
    ],
    "current": ["temperature_2m", "relative_humidity_2m"],
    "timezone": "Asia/Tokyo",
    "past_days": 7,
}
responses = openmeteo.weather_api(url, params=params)

# Process first location. Add a for-loop for multiple locations or weather models
response = responses[0]
print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
print(f"Elevation: {response.Elevation()} m asl")
print(f"Timezone: {response.Timezone()}{response.TimezoneAbbreviation()}")
print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")

# Process current data. The order of variables needs to be the same as requested.
current = response.Current()
current_temperature_2m = current.Variables(0).Value()
current_relative_humidity_2m = current.Variables(1).Value()

print(f"\nCurrent time: {current.Time()}")
print(f"Current temperature_2m: {current_temperature_2m}")
print(f"Current relative_humidity_2m: {current_relative_humidity_2m}")

# Process hourly data. The order of variables needs to be the same as requested.
hourly = response.Hourly()
hourly_soil_temperature_0cm = hourly.Variables(0).ValuesAsNumpy()
hourly_soil_temperature_6cm = hourly.Variables(1).ValuesAsNumpy()
hourly_soil_temperature_18cm = hourly.Variables(2).ValuesAsNumpy()
hourly_soil_moisture_0_to_1cm = hourly.Variables(3).ValuesAsNumpy()
hourly_soil_moisture_1_to_3cm = hourly.Variables(4).ValuesAsNumpy()
hourly_soil_moisture_3_to_9cm = hourly.Variables(5).ValuesAsNumpy()
hourly_soil_moisture_9_to_27cm = hourly.Variables(6).ValuesAsNumpy()
hourly_et0_fao_evapotranspiration = hourly.Variables(7).ValuesAsNumpy()
hourly_vapour_pressure_deficit = hourly.Variables(8).ValuesAsNumpy()
hourly_shortwave_radiation = hourly.Variables(9).ValuesAsNumpy()
hourly_sunshine_duration = hourly.Variables(10).ValuesAsNumpy()
hourly_wet_bulb_temperature_2m = hourly.Variables(11).ValuesAsNumpy()
hourly_global_tilted_irradiance = hourly.Variables(12).ValuesAsNumpy()

hourly_data = {
    "date": pd.date_range(
        start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
        end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
        freq=pd.Timedelta(seconds=hourly.Interval()),
        inclusive="left",
    ).tz_convert(response.Timezone().decode())
}

hourly_data["soil_temperature_0cm"] = hourly_soil_temperature_0cm
hourly_data["soil_temperature_6cm"] = hourly_soil_temperature_6cm
hourly_data["soil_temperature_18cm"] = hourly_soil_temperature_18cm
hourly_data["soil_moisture_0_to_1cm"] = hourly_soil_moisture_0_to_1cm
hourly_data["soil_moisture_1_to_3cm"] = hourly_soil_moisture_1_to_3cm
hourly_data["soil_moisture_3_to_9cm"] = hourly_soil_moisture_3_to_9cm
hourly_data["soil_moisture_9_to_27cm"] = hourly_soil_moisture_9_to_27cm
hourly_data["et0_fao_evapotranspiration"] = hourly_et0_fao_evapotranspiration
hourly_data["vapour_pressure_deficit"] = hourly_vapour_pressure_deficit
hourly_data["shortwave_radiation"] = hourly_shortwave_radiation
hourly_data["sunshine_duration"] = hourly_sunshine_duration
hourly_data["wet_bulb_temperature_2m"] = hourly_wet_bulb_temperature_2m
hourly_data["global_tilted_irradiance"] = hourly_global_tilted_irradiance

hourly_dataframe = pd.DataFrame(data=hourly_data)
print("\nHourly data\n", hourly_dataframe)

# Process daily data. The order of variables needs to be the same as requested.
daily = response.Daily()
daily_temperature_2m_max = daily.Variables(0).ValuesAsNumpy()
daily_temperature_2m_min = daily.Variables(1).ValuesAsNumpy()
daily_precipitation_sum = daily.Variables(2).ValuesAsNumpy()
daily_sunshine_duration = daily.Variables(3).ValuesAsNumpy()
daily_shortwave_radiation_sum = daily.Variables(4).ValuesAsNumpy()
daily_wind_speed_10m_max = daily.Variables(5).ValuesAsNumpy()
daily_wind_gusts_10m_max = daily.Variables(6).ValuesAsNumpy()

daily_data = {
    "date": pd.date_range(
        start=pd.to_datetime(daily.Time(), unit="s", utc=True),
        end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
        freq=pd.Timedelta(seconds=daily.Interval()),
        inclusive="left",
    ).tz_convert(response.Timezone().decode())
}

daily_data["temperature_2m_max"] = daily_temperature_2m_max
daily_data["temperature_2m_min"] = daily_temperature_2m_min
daily_data["precipitation_sum"] = daily_precipitation_sum
daily_data["sunshine_duration"] = daily_sunshine_duration
daily_data["shortwave_radiation_sum"] = daily_shortwave_radiation_sum
daily_data["wind_speed_10m_max"] = daily_wind_speed_10m_max
daily_data["wind_gusts_10m_max"] = daily_wind_gusts_10m_max

daily_dataframe = pd.DataFrame(data=daily_data)
print("\nDaily data\n", daily_dataframe)

avg_max_temp = daily_dataframe["temperature_2m_max"].mean()
total_precipitation = daily_dataframe["precipitation_sum"].sum()

print(f"\n--- Data summary ---")
print(f"Average maximum temperature during the period: {avg_max_temp:.1f} °C")
print(f"Total rainfall during the period: {total_precipitation:.1f} mm")


def calculate_dairy_suitability(temp, rain):
    score = 100

    if temp > 25.0:
        score -= (temp - 25.0) * 15

    if rain < 20.0:
        score -= 20

    return max(0, min(100, score))


suitability_score = calculate_dairy_suitability(avg_max_temp, total_precipitation)

print(f"Suitability for dairy and pasture: {suitability_score:.0f} %")
