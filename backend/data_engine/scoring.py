import pandas as pd
from .crop_criteria import CROP_CRITERIA


def calculate_suitability_scores(daily_dataframe: pd.DataFrame) -> dict:

    daily_dataframe["year"] = daily_dataframe["date"].dt.year

    annual_stats = daily_dataframe.groupby("year").agg(
        {
            "precipitation_sum": "sum",
            "sunshine_duration": "sum",
            "temperature_2m_max": "mean",
            "temperature_2m_min": "mean",
            "wind_gusts_10m_max": "max",
        }
    )

    avg_annual_precip = annual_stats["precipitation_sum"].mean()
    avg_annual_sunshine_hours = (annual_stats["sunshine_duration"].mean()) / 3600
    avg_max_temp = annual_stats["temperature_2m_max"].mean()
    avg_min_temp = annual_stats["temperature_2m_min"].mean()
    max_wind_gust = annual_stats["wind_gusts_10m_max"].max()

    results = {}

    for crop_id, criteria in CROP_CRITERIA.items():
        score = 100

        if avg_annual_precip < criteria["precipitation_sum_annual_min"]:
            deficit = criteria["precipitation_sum_annual_min"] - avg_annual_precip
            score -= (deficit / 100) * 5
        elif avg_annual_precip > criteria["precipitation_sum_annual_max"]:
            excess = avg_annual_precip - criteria["precipitation_sum_annual_max"]
            score -= (excess / 100) * 5

        if avg_max_temp > criteria["temperature_2m_opt_max"]:
            score -= (avg_max_temp - criteria["temperature_2m_opt_max"]) * 10
        elif avg_max_temp < criteria["temperature_2m_opt_min"]:
            score -= (criteria["temperature_2m_opt_min"] - avg_max_temp) * 10

        if avg_min_temp < criteria["temperature_2m_limit_min"]:
            score -= 50

        if avg_annual_sunshine_hours < criteria["sunshine_duration_hours_min"]:
            deficit = (
                criteria["sunshine_duration_hours_min"] - avg_annual_sunshine_hours
            )
            score -= (deficit / 100) * 5

        if max_wind_gust > criteria["wind_gusts_10m_max_limit"]:
            excess = max_wind_gust - criteria["wind_gusts_10m_max_limit"]
            score -= excess * 2

        final_score = max(0, min(100, int(score)))

        results[crop_id] = {"name": criteria["name"], "score": final_score}

    return results
