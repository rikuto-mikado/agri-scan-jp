import pandas as pd
from .crop_criteria import CROP_CRITERIA


def calculate_suitability_scores(
    daily_dataframe: pd.DataFrame, lat: float = None, lon: float = None
) -> dict:

    # Prepare helper columns
    daily_dataframe["year"] = daily_dataframe["date"].dt.year
    daily_dataframe["month"] = daily_dataframe["date"].dt.month

    # Base annual aggregations (may be from partial years)
    annual_stats = daily_dataframe.groupby("year").agg(
        {
            "precipitation_sum": "sum",
            "sunshine_duration": "sum",
            "temperature_2m_max": "mean",
            "temperature_2m_min": "mean",
            "wind_gusts_10m_max": "max",
        }
    )

    # Count observed days per year so partial-year data can be annualized
    days_per_year = daily_dataframe.groupby("year")["date"].count()

    # Annualize precipitation and sunshine if the observation period is shorter than a full year
    # (avoid underestimating annual totals when only part of a year was requested)
    annual_precip_annualized = annual_stats["precipitation_sum"] * 365.0 / days_per_year
    annual_sunshine_annualized = (
        annual_stats["sunshine_duration"] * 365.0 / days_per_year
    )

    # Use the mean of annualized values across years
    avg_annual_precip = annual_precip_annualized.mean()
    # sunshine is returned by API in seconds — convert to hours after annualizing
    avg_annual_sunshine_hours = (annual_sunshine_annualized.mean()) / 3600.0

    # For maximum temperature, use a warm-season metric: for each year, take the mean of the
    # up-to-4 warmest months' daily maximum temperatures, then average across years.
    monthly_max_mean = daily_dataframe.groupby(["year", "month"])[
        "temperature_2m_max"
    ].mean()

    def warm_months_mean_for_year(g):
        # g is a Series indexed by month for a single year
        if g.size == 0:
            return float("nan")
        n = min(4, g.size)
        return g.nlargest(n).mean()

    warm_months_per_year = monthly_max_mean.groupby(level=0).apply(
        warm_months_mean_for_year
    )
    avg_max_temp = warm_months_per_year.mean()

    # Keep annual mean of minimum temperatures (used for cold-limit checks)
    avg_min_temp = annual_stats["temperature_2m_min"].mean()

    # Max wind gust across all years
    max_wind_gust = annual_stats["wind_gusts_10m_max"].max()

    if lat is not None and lon is not None:
        print(f"=== Data used for calculations ({lat}, {lon}) ===")
    else:
        print("=== Data used for calculations ===")

    print(f"Observed years: {len(annual_stats)}")
    print(f"Observed days per year (sample): {dict(days_per_year.head())}")
    print(f"Average annual precipitation (annualized): {avg_annual_precip:.1f} mm")
    print(
        f"Average annual sunshine hours (annualized): {avg_annual_sunshine_hours:.1f} hours"
    )
    print(f"Warm-season mean maximum temperature: {avg_max_temp:.1f} ℃")
    print(f"Annual mean minimum temperature: {avg_min_temp:.1f} ℃")
    print(f"Maximum wind gust: {max_wind_gust:.1f} km/h")
    print("====================================")

    results = {}

    for crop_id, criteria in CROP_CRITERIA.items():
        score = 100
        print(f"\n--- {criteria['name']} ---")

        # Precipitation: compare to annualized values
        if avg_annual_precip < criteria["precipitation_sum_annual_min"]:
            deficit = criteria["precipitation_sum_annual_min"] - avg_annual_precip
            score -= (deficit / 100.0) * 5.0
        # elif avg_annual_precip > criteria["precipitation_sum_annual_max"]:
        #     excess = avg_annual_precip - criteria["precipitation_sum_annual_max"]
        #     score -= (excess / 100.0) * 5.0

        # Temperature: use warm-season max metric and soften degree penalty
        if avg_max_temp > criteria["temperature_2m_opt_max"]:
            score -= (avg_max_temp - criteria["temperature_2m_opt_max"]) * 5.0
        elif avg_max_temp < criteria["temperature_2m_opt_min"]:
            score -= (criteria["temperature_2m_opt_min"] - avg_max_temp) * 5.0

        # Cold limit: reduce single-shot penalty to be less severe
        if avg_min_temp < criteria["temperature_2m_limit_min"]:
            score -= 30

        # Sunshine: compare annualized hours
        if avg_annual_sunshine_hours < criteria["sunshine_duration_hours_min"]:
            deficit = (
                criteria["sunshine_duration_hours_min"] - avg_annual_sunshine_hours
            )
            score -= (deficit / 100.0) * 5.0

        # Wind gusts: keep existing logic
        # if max_wind_gust > criteria["wind_gusts_10m_max_limit"]:
        #     excess = max_wind_gust - criteria["wind_gusts_10m_max_limit"]
        #     score -= excess * 2.0

        final_score = max(0, min(100, int(score)))
        print(f"Final suitability score: {final_score}")

        results[crop_id] = {"name": criteria["name"], "score": final_score}

    return results
