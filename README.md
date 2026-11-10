# Assignment 2

## Introduction

This script downloads Divvy bike data, cleans the data, analyzes ridership by whether a rider has a membership or not, and builds a baseline model for predicting ride time.

## Clone Repo

`git clone https://github.com/Typical-OutOfBounds/week2-assignment-aidan-lane.git`

`cd week2-assignment-aidan-lane`

## Instructions

This script was built using Python 3.13

The matplotlib and pandas packages are needed and can be installed by running `python -m pip install -r requirements.txt`

### Data Loading

run `python data_loader.py 202101-divvy-tripdata --output-dir outputs`

By default, the loader downloads the `202101-divvy-tripdata` archive and extracts `202101-divvy-tripdata.csv` to the current directory.

### Data Cleaning

run `python3 data_cleaner.py outputs/202101-divvy-tripdata.csv --output outputs/cleaned_data.csv`

By default, the cleaner reads `202101-divvy-tripdata.csv` and writes `cleaned_data.csv` in the current directory.

### Analyzing Data

run `python3 analyze_data.py outputs/cleaned_data.csv --output outputs/rider_chart.jpg`

By default, the analyzer reads `cleaned_data.csv` and writes `rider_chart.jpg` in the current directory.

### Modeling Data

run `python3 simple_model.py outputs/cleaned_data.csv > outputs/model_metrics.txt`

By default, the model reads `cleaned_data.csv` from the current directory and prints its metrics to the terminal.

## Description

The first script downloads a month of Divvy data. The next script cleans the data and adds ride duration and day type. The third script makes a bar chart comparing average ride duration by rider type and weekday versus weekend. The last script uses earlier rides to find a median for each group and an overall median. It compares how well both predict ride duration on the final seven days.

The scripts can be run separately and are ready to be put into a full pipeline. Run them in the order shown above so each one has the data it needs.
