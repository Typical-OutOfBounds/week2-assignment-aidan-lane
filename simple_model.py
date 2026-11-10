"""Run simple model on Divvy bike data using median ride duration"""

import pandas as pd

def run_model(rides):
    """
    Run baseline model using median trip time
    """
    test_start = rides["started_at"].max().normalize() - pd.Timedelta(days=6)
    train_rides = rides.loc[rides["ended_at"] < test_start]
    test_rides = rides.loc[rides["started_at"] >= test_start].copy()

    model_features = ["rider_type", "day_type"]
    baseline_minutes = train_rides["duration_minutes"].median()
    group_medians = train_rides.groupby(model_features)["duration_minutes"].median()

    test_rides = test_rides.join(
        group_medians.rename("predicted_minutes"), on=model_features
    )
    test_rides["predicted_minutes"] = test_rides["predicted_minutes"].fillna(
        baseline_minutes
    )

    actual_minutes = test_rides["duration_minutes"]
    baseline_mae = (actual_minutes - baseline_minutes).abs().mean()
    model_mae = (actual_minutes - test_rides["predicted_minutes"]).abs().mean()

    print(f"Test trips starting on or after {test_start:%Y-%m-%d}: {len(test_rides):,}")
    print(f"Baseline mean absolute error: {baseline_mae:.2f} minutes")
    print(f"Model mean absolute error: {model_mae:.2f} minutes")

if __name__ == "__main__":
    file_path = "cleaned_data.csv"

    df = pd.read_csv(file_path, parse_dates=["started_at", "ended_at"])
    run_model(df)