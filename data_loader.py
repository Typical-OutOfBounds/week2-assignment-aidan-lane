from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile

trip_columns = ["ride_id", "member_casual", "started_at", "ended_at"]

"""
Downloads a file from the divvy archive and saves it to a local directory.

Returns the file path it saved to
"""
def download_bike_data(arcive_name):
    archive_url = f"https://divvy-tripdata.s3.amazonaws.com/{archive_name}.zip"

    with urlopen(archive_url, timeout=30) as response:
        archive_bytes = response.read()

    # Open the trip CSV by name because the ZIP also contains macOS metadata.
    with ZipFile(BytesIO(archive_bytes)) as archive:
        file_path = archive.extract(f"{archive_name}.csv")

    return file_path

if __name__ == "__main__":
    import pandas as pd

    archive_name = "202101-divvy-tripdata"

    file_path = download_bike_data(arcive_name=archive_name)

    df = pd.read_csv(file_path)

    print("Downloaded data to:", file_path)
    print("Downloaded {} rows".format(len(df)))
