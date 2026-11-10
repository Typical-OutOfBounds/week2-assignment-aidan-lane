import pandas as pd

def clean_data(rides, write=False):
    rides = rides.rename(columns={"member_casual": "rider_type"})
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
    #print(f"Kept {len(rides):,} rides and removed {len(raw_rides) - len(rides):,} rows.")
    #rides.head()

    if write:
        rides.to_csv("cleaned_data.csv")

    return rides

if __name__ == "__main__":
    file_path = "202101-divvy-tripdata.csv"

    df = pd.read_csv(file_path)
    clean_data(df, write=True)
