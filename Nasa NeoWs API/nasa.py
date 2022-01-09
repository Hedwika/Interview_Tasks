# Write a simple Python script/program that takes two date arguments and retrieves the list of near-Earth space objects
# approaching Earth in that time interval. Output the list of the objects, sorted by their closest approach distance,
# in an aligned tabular format, the object name, size estimate, time and distance of the closest encounter.
#
# The data should come from the API of NeoWs service at https://api.nasa.gov/ (free registration required).

import requests
import pandas as pd

desired_width = 1000
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns',100)
pd.set_option('max_colwidth', 400)

response = requests.get("https://api.nasa.gov/neo/rest/v1/feed?start_date=2020-01-01&end_date=2020-01-06&api_key=qVNuxuWB0l7e3SRfNz8USva2h3IOUyj7HaxutEc8")
print(response.status_code)

json_data = response.json()
df = pd.DataFrame(json_data)
df.to_json('nasa_neows.json')

planets_df = pd.read_json("nasa_neows.json")
planets_df = planets_df[planets_df['near_earth_objects'].notna()]

def dates(df, column, row):
    date = df[column][row]
    date = pd.json_normalize(date, max_level=2)
    date = date[['name','close_approach_data','estimated_diameter.meters.estimated_diameter_min',
                 'estimated_diameter.meters.estimated_diameter_max']]
    date["size_estimate_m"] = (date['estimated_diameter.meters.estimated_diameter_min'] +
                                date['estimated_diameter.meters.estimated_diameter_max'])/2

    times = []
    closest_approach_distance = []
    for idx, object in date.iterrows():
        close_approach_data = date["close_approach_data"][idx]
        close_approach_data = pd.json_normalize(close_approach_data, max_level=2)
        object_closest_approach_distance = close_approach_data["miss_distance.kilometers"].values
        object_closest_approach_distance = object_closest_approach_distance[0]
        full_date = close_approach_data["close_approach_date_full"].values
        full_date = full_date[0]
        times.append(full_date)
        closest_approach_distance.append(object_closest_approach_distance)

    date["time"] = times
    date["closest_approach_distance_m"] = closest_approach_distance
    date = date.drop(columns=['estimated_diameter.meters.estimated_diameter_min',
                              'estimated_diameter.meters.estimated_diameter_max',
                              'close_approach_data'])
    return date

final_planets_df = pd.DataFrame(columns=["name", "size_estimate_m", "time", "closest_approach_distance_m"])

for idx, date in planets_df.iterrows():
    df = dates(planets_df, 'near_earth_objects', idx)
    final_planets_df = pd.concat([final_planets_df, df], ignore_index=True)

final_planets_df["time"] = final_planets_df["time"].apply(pd.to_datetime)
final_planets_df["closest_approach_distance_m"] = final_planets_df["closest_approach_distance_m"].apply(pd.to_numeric)

def find_nearest_planets(start, end):
    result = (final_planets_df[(final_planets_df['time'] > start) & (final_planets_df["time"] < end)])\
        .sort_values(by=['closest_approach_distance_m']).reset_index()
    result = result.drop(columns="index")
    result = pd.DataFrame(result)
    print(result)

find_nearest_planets("2020-01-02 02:00:00", "2020-01-03 12:00:00")