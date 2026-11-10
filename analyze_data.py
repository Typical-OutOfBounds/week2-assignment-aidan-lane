"""Analyzes Divvy bike data"""

from os import PathLike

import matplotlib.pyplot as plt
import pandas as pd

def summarize_rides(rides: pd.DataFrame) -> pd.DataFrame:
    """
    Summarize rides by rider type and round the output
    """
    summary = rides.groupby(["rider_type", "day_type"]).agg(
        ride_count=("ride_id", "size"),
        mean_minutes=("duration_minutes", "mean"),
        median_minutes=("duration_minutes", "median"),
    )
    rounded_summary = summary.round(1)

    return rounded_summary

def compare_groups(summary: pd.DataFrame, output_path: str | PathLike[str] | None = None) -> None:
    """
    Plot summarized rides by rider type
    """
    mean_by_day = summary["mean_minutes"].unstack("day_type")
    ax = mean_by_day.plot.bar(
        figsize=(7, 4),
        rot=0,
        color=["#326D9A", "#DF923A"],
        title="Average Divvy ride duration",
    )
    ax.set_xlabel("Rider type")
    ax.set_ylabel("Mean duration (minutes)")
    ax.legend(title="Trip start day")

    if output_path is not None:
        plt.savefig(output_path)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    import argparse
    from pathlib import Path

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "input_csv", help="Cleaned Divvy trip CSV path", nargs="?", default="cleaned_data.csv"
    )
    parser.add_argument(
        "-o", "--output", type=Path, default="rider_chart.jpg",
        help="Output image path (default: rider_chart.jpg)",
    )
    args = parser.parse_args()

    df = pd.read_csv(args.input_csv, parse_dates=["started_at", "ended_at"])
    summarize_rides = summarize_rides(df)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    compare_groups(summarize_rides, args.output)
