"""Clean Divvy bike trip data"""

from os import PathLike

import pandas as pd

def clean_data(
    raw_rides: pd.DataFrame, output_path: str | PathLike[str] | None = None
) -> pd.DataFrame:
    """
    Cleans divvy bike data

    returns the cleaned dataframe and writes the data to and output path if specified
    """
    rides = raw_rides.rename(columns={"member_casual": "rider_type"})
    rides["rider_type"] = rides["rider_type"].str.strip().str.lower().replace("", pd.NA)
    rides = rides.drop_duplicates()

    # Invalid timestamp strings become missing values so they can be filtered together.
    rides["started_at"] = pd.to_datetime(rides["started_at"], errors="coerce")
    rides["ended_at"] = pd.to_datetime(rides["ended_at"], errors="coerce")
    rides = rides.dropna(subset=["rider_type", "started_at", "ended_at"]).copy()

    rides["duration_minutes"] = (
        (rides["ended_at"] - rides["started_at"]).dt.total_seconds() / 60
    )
    rides = rides.loc[rides["duration_minutes"] > 0].copy()
    rides["day_type"] = rides["started_at"].dt.dayofweek.ge(5).map(
        {False: "Weekday", True: "Weekend"}
    )
    print(f"Kept {len(rides):,} rides and removed {len(raw_rides) - len(rides):,} rows.")

    if output_path is not None:
        rides.to_csv(output_path)

    return rides

if __name__ == "__main__":
    import argparse
    from pathlib import Path

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "input_csv", help="Divvy trip CSV path", nargs="?", default="202101-divvy-tripdata.csv"
    )
    parser.add_argument(
        "-o", "--output", type=Path, default="cleaned_data.csv",
        help="Output CSV path (default: cleaned_data.csv)",
    )
    args = parser.parse_args()

    df = pd.read_csv(args.input_csv)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    clean_data(df, args.output)
