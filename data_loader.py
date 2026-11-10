"""Download Divvy bike trip data."""

from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile

trip_columns = ["ride_id", "member_casual", "started_at", "ended_at"]

def download_bike_data(archive_name):
    """Download a Divvy archive and return the path to its extracted CSV."""
    archive_url = f"https://divvy-tripdata.s3.amazonaws.com/{archive_name}.zip"

    with urlopen(archive_url, timeout=30) as response:
        archive_bytes = response.read()

    # Open the trip CSV by name because the ZIP also contains macOS metadata.
    with ZipFile(BytesIO(archive_bytes)) as archive:
        return archive.extract(f"{archive_name}.csv")


if __name__ == "__main__":
    import argparse
    import pandas as pd

    parser = argparse.ArgumentParser()
    parser.add_argument("input_archive", help="divvy archive name", nargs="?", default="202101-divvy-tripdata")

    args = parser.parse_args()

    file_path = download_bike_data(args.input_archive)

    df = pd.read_csv(file_path)

    print("Downloaded data to:", file_path)
    print(f"Downloaded {len(df)} rows")
