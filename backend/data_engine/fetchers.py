import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession(".cache", expire_after=-1)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)


def get_weather_data(
    lat: float, lon: float, start_date: str = "2020-01-01", end_date: str = "2024-12-31"
) -> pd.DataFrame:
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start_date,
        "end_date": end_date,
        "daily": [
            "temperature_2m_max",
            "temperature_2m_min",
            "sunshine_duration",
            "precipitation_sum",
            "wind_speed_10m_max",
            "wind_gusts_10m_max",
            "shortwave_radiation_sum",
        ],
        "hourly": [
            "soil_temperature_0_to_7cm",
            "soil_temperature_7_to_28cm",
            "soil_moisture_0_to_7cm",
            "soil_moisture_7_to_28cm",
            "et0_fao_evapotranspiration",
            "vapour_pressure_deficit",
            "shortwave_radiation",
            "global_tilted_irradiance",
            "temperature_2m",
            "relative_humidity_2m",
        ],
        "timezone": "Asia/Tokyo",
    }

    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]

    daily = response.Daily()
    daily_data = {
        "date": pd.date_range(
            start=pd.to_datetime(daily.Time(), unit="s", utc=True),
            end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=daily.Interval()),
            inclusive="left",
        ).tz_convert(response.Timezone().decode())
    }

    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    # url = "https://archive-api.open-meteo.com/v1/archive"
    # params = {
    #     "latitude": 35.41,
    #     "longitude": 139.41,
    #     "start_date": "2020-01-01",
    #     "end_date": "2024-12-31",
    #     "daily": [
    #         "temperature_2m_max",
    #         "temperature_2m_min",
    #         "sunshine_duration",
    #         "precipitation_sum",
    #         "wind_speed_10m_max",
    #         "wind_gusts_10m_max",
    #         "shortwave_radiation_sum",
    #     ],
    #     "hourly": [
    #         "soil_temperature_0_to_7cm",
    #         "soil_temperature_7_to_28cm",
    #         "soil_moisture_0_to_7cm",
    #         "soil_moisture_7_to_28cm",
    #         "et0_fao_evapotranspiration",
    #         "vapour_pressure_deficit",
    #         "shortwave_radiation",
    #         "global_tilted_irradiance",
    #         "temperature_2m",
    #         "relative_humidity_2m",
    #     ],
    #     "timezone": "Asia/Tokyo",
    # }
    # responses = openmeteo.weather_api(url, params=params)

    # # Process first location. Add a for-loop for multiple locations or weather models
    # response = responses[0]
    print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
    print(f"Elevation: {response.Elevation()} m asl")
    print(f"Timezone: {response.Timezone()}{response.TimezoneAbbreviation()}")
    print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")

    # Process hourly data. The order of variables needs to be the same as requested.
    hourly = response.Hourly()
    hourly_soil_temperature_0_to_7cm = hourly.Variables(0).ValuesAsNumpy()
    hourly_soil_temperature_7_to_28cm = hourly.Variables(1).ValuesAsNumpy()
    hourly_soil_moisture_0_to_7cm = hourly.Variables(2).ValuesAsNumpy()
    hourly_soil_moisture_7_to_28cm = hourly.Variables(3).ValuesAsNumpy()
    hourly_et0_fao_evapotranspiration = hourly.Variables(4).ValuesAsNumpy()
    hourly_vapour_pressure_deficit = hourly.Variables(5).ValuesAsNumpy()
    hourly_shortwave_radiation = hourly.Variables(6).ValuesAsNumpy()
    hourly_global_tilted_irradiance = hourly.Variables(7).ValuesAsNumpy()
    hourly_temperature_2m = hourly.Variables(8).ValuesAsNumpy()
    hourly_relative_humidity_2m = hourly.Variables(9).ValuesAsNumpy()

    hourly_data = {
        "date": pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left",
        ).tz_convert(response.Timezone().decode())
    }

    hourly_data["soil_temperature_0_to_7cm"] = hourly_soil_temperature_0_to_7cm
    hourly_data["soil_temperature_7_to_28cm"] = hourly_soil_temperature_7_to_28cm
    hourly_data["soil_moisture_0_to_7cm"] = hourly_soil_moisture_0_to_7cm
    hourly_data["soil_moisture_7_to_28cm"] = hourly_soil_moisture_7_to_28cm
    hourly_data["et0_fao_evapotranspiration"] = hourly_et0_fao_evapotranspiration
    hourly_data["vapour_pressure_deficit"] = hourly_vapour_pressure_deficit
    hourly_data["shortwave_radiation"] = hourly_shortwave_radiation
    hourly_data["global_tilted_irradiance"] = hourly_global_tilted_irradiance
    hourly_data["temperature_2m"] = hourly_temperature_2m
    hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m

    hourly_dataframe = pd.DataFrame(data=hourly_data)
    print("\nHourly data\n", hourly_dataframe)

    # Process daily data. The order of variables needs to be the same as requested.
    daily = response.Daily()
    daily_temperature_2m_max = daily.Variables(0).ValuesAsNumpy()
    daily_temperature_2m_min = daily.Variables(1).ValuesAsNumpy()
    daily_sunshine_duration = daily.Variables(2).ValuesAsNumpy()
    daily_precipitation_sum = daily.Variables(3).ValuesAsNumpy()
    daily_wind_speed_10m_max = daily.Variables(4).ValuesAsNumpy()
    daily_wind_gusts_10m_max = daily.Variables(5).ValuesAsNumpy()
    daily_shortwave_radiation_sum = daily.Variables(6).ValuesAsNumpy()

    # daily_data = {
    #     "date": pd.date_range(
    #         start=pd.to_datetime(daily.Time(), unit="s", utc=True),
    #         end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
    #         freq=pd.Timedelta(seconds=daily.Interval()),
    #         inclusive="left",
    #     ).tz_convert(response.Timezone().decode())
    # }

    daily_data["temperature_2m_max"] = daily_temperature_2m_max
    daily_data["temperature_2m_min"] = daily_temperature_2m_min
    daily_data["sunshine_duration"] = daily_sunshine_duration
    daily_data["precipitation_sum"] = daily_precipitation_sum
    daily_data["wind_speed_10m_max"] = daily_wind_speed_10m_max
    daily_data["wind_gusts_10m_max"] = daily_wind_gusts_10m_max
    daily_data["shortwave_radiation_sum"] = daily_shortwave_radiation_sum

    daily_dataframe = pd.DataFrame(data=daily_data)
    print("\nDaily data\n", daily_dataframe)

    return daily_dataframe
