"""
Agricultural Land Suitability Criteria
Aligned with Open-Meteo API variable names.
"""

CROP_CRITERIA = {
    # ==========================================
    # GRAINS
    # ==========================================
    "rice_paddy": {
        "name": "Rice (Paddy)",
        "temperature_2m_opt_min": 20.0,
        "temperature_2m_opt_max": 30.0,
        "temperature_2m_limit_min": 15.0,
        "precipitation_sum_annual_min": 1200.0,
        "precipitation_sum_annual_max": 3000.0,
        "sunshine_duration_hours_min": 1300.0,
        "wind_gusts_10m_max_limit": 25.0,
    },
    # ==========================================
    # ORCHARDS
    # ==========================================
    "orchard_citrus": {
        "name": "Orchard (Citrus/Satsuma Mandarin)",
        "temperature_2m_opt_min": 15.0,
        "temperature_2m_opt_max": 30.0,
        "temperature_2m_limit_min": -3.0,
        "precipitation_sum_annual_min": 1200.0,
        "precipitation_sum_annual_max": 2000.0,
        "sunshine_duration_hours_min": 1200.0,
        "wind_gusts_10m_max_limit": 20.0,
    },
    "orchard_apple": {
        "name": "Orchard (Apple)",
        "temperature_2m_opt_min": 15.0,
        "temperature_2m_opt_max": 25.0,
        "temperature_2m_limit_min": -20.0,
        "precipitation_sum_annual_min": 800.0,
        "precipitation_sum_annual_max": 1500.0,
        "sunshine_duration_hours_min": 1500.0,
        "wind_gusts_10m_max_limit": 15.0,
    },
    "orchard_grape": {
        "name": "Orchard (Grape)",
        "temperature_2m_opt_min": 18.0,
        "temperature_2m_opt_max": 28.0,
        "temperature_2m_limit_min": -15.0,
        "precipitation_sum_annual_min": 500.0,
        "precipitation_sum_annual_max": 1200.0,
        "sunshine_duration_hours_min": 1400.0,
        "wind_gusts_10m_max_limit": 20.0,
    },
    # ==========================================
    # VEGETABLES
    # ==========================================
    "veg_root_potato": {
        "name": "Root Vegetable (Potato)",
        "temperature_2m_opt_min": 15.0,
        "temperature_2m_opt_max": 21.0,
        "temperature_2m_limit_min": 0.0,
        "precipitation_sum_annual_min": 400.0,
        "precipitation_sum_annual_max": 1000.0,
        "sunshine_duration_hours_min": 1000.0,
        "wind_gusts_10m_max_limit": 30.0,
    },
    "veg_fruit_tomato": {
        "name": "Fruit Vegetable (Tomato/Open Field)",
        "temperature_2m_opt_min": 20.0,
        "temperature_2m_opt_max": 28.0,
        "temperature_2m_limit_min": 10.0,
        "precipitation_sum_annual_min": 400.0,
        "precipitation_sum_annual_max": 1000.0,
        "sunshine_duration_hours_min": 1500.0,
        "wind_gusts_10m_max_limit": 15.0,
    },
    # ==========================================
    # DAIRY & PASTURE
    # ==========================================
    "dairy_cool_climate": {
        "name": "Dairy (Cool Climate Pasture/Holstein)",
        "temperature_2m_opt_min": 5.0,
        "temperature_2m_opt_max": 22.0,
        "temperature_2m_limit_min": -20.0,
        "precipitation_sum_annual_min": 800.0,
        "precipitation_sum_annual_max": 1800.0,
        "sunshine_duration_hours_min": 1000.0,
        "wind_gusts_10m_max_limit": 30.0,
    },
}
