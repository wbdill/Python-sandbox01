import sqlite3
import requests
import pandas as pd
from datetime import datetime

# API endpoints
first_api_url = "https://api.weather.gov/points/36.0063,-86.7909"
#first_api_url = "https://api.weather.gov/points/33.5508,-88.4865"

# Fetch data from the first API
response = requests.get(first_api_url)
if response.status_code != 200:
    raise Exception("Failed to fetch data from first API")

data = response.json()

# Extract required fields with snake_case keys
forecast_data = {
    "city": data["properties"]["relativeLocation"]["properties"]["city"],
    "state": data["properties"]["relativeLocation"]["properties"]["state"],
    "radar_station": data["properties"]["radarStation"],
    "created": datetime.now(),
    "forecast": data["properties"]["forecast"],
    "forecast_hourly": data["properties"]["forecastHourly"],
    "forecast_grid_data": data["properties"]["forecastGridData"]
}

# Create a DataFrame
calls_df = pd.DataFrame([forecast_data])

# Connect to SQLite database and create "calls" table
conn = sqlite3.connect('ApiWeather/Forecasts.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS calls (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        city TEXT,
        state TEXT,
        radar_station TEXT,
        created TEXT,
        forecast TEXT,
        forecast_hourly TEXT,
        forecast_grid_data TEXT

    )
''')

# Insert call data
calls_df.to_sql('calls', conn, if_exists='append', index=False)

# Get the last inserted row ID
cursor.execute("SELECT last_insert_rowid()")
call_id = cursor.fetchone()[0]

# Fetch the second API using forecast URL
second_api_url = data["properties"]["forecast"]
response = requests.get(second_api_url)
if response.status_code != 200:
    raise Exception("Failed to fetch data from second API")

forecast_data = response.json()

# Extract "periods" forecast details
periods = forecast_data["properties"]["periods"]
forecasts_df = pd.DataFrame(periods)[
    ["number", "name", "startTime", "endTime", "isDaytime", "temperature",
     "windSpeed", "icon", "shortForecast", "detailedForecast"]
]

# Rename columns to snake_case
forecasts_df.rename(columns={
    "number": "number",
    "name": "name",
    "startTime": "start_time",
    "endTime": "end_time",
    "isDaytime": "is_daytime",
    "temperature": "temperature",
    "windSpeed": "wind_speed",
    "icon": "icon",
    "shortForecast": "short_forecast",
    "detailedForecast": "detailed_forecast"
}, inplace=True)

# Add foreign key column to associate with "calls" table
forecasts_df["call_id"] = call_id

# Create "forecasts" table with snake_case columns
cursor.execute('''
    CREATE TABLE IF NOT EXISTS forecasts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        call_id INTEGER,
        number INTEGER,
        name TEXT,
        start_time TEXT,
        end_time TEXT,
        is_daytime BOOLEAN,
        temperature INTEGER,
        wind_speed TEXT,
        icon TEXT,
        short_forecast TEXT,
        detailed_forecast TEXT,
        FOREIGN KEY (call_id) REFERENCES calls(id)
    )
''')

# Insert forecast data
forecasts_df.to_sql('forecasts', conn, if_exists='append', index=False)

# Commit and close connection
conn.commit()
conn.close()

print(f"Inserted call ID: {call_id}")
print("Forecast data successfully inserted into SQLite database.")
