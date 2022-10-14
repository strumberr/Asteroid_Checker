import requests
import os
from dotenv import load_dotenv
import json
from datetime import date
import datetime
import math

load_dotenv()

api_key = os.getenv('API_KEY')

def nasa_api(start_date, end_date):

    
    list1 = []

    list2 = []

    global list_asteroid_names

    list_asteroid_names = []


    r = requests.get(f'https://api.nasa.gov/neo/rest/v1/feed?start_date={start_date}&end_date={end_date}&api_key={api_key}')

    r_dict = r.json()

    json_object = json.dumps(r_dict, indent = 4) 

    print(json_object)

    json_main = json.loads(json_object)

    with open('jsonthing.txt', 'w') as f:
        f.write(str(json_object))

    print(json_main)


    loop_iteration = 0

    for el in json_main["near_earth_objects"][f"{start_date}"]:
        json_object = json.dumps(el, indent = 4)
        json_all = json.loads(json_object)

        asteroid_ID = json_all["id"]
        asteroid_name = json_all["name"]
        asteroid_diameter_min = json_all["estimated_diameter"]["meters"]["estimated_diameter_min"]
        asteroid_diameter_max = json_all["estimated_diameter"]["meters"]["estimated_diameter_max"]
        asteroid_approach_time = json_all["close_approach_data"][0]["close_approach_date_full"]
        asteroid_kmh = json_all["close_approach_data"][0]["relative_velocity"]["kilometers_per_hour"]
        asteroid_miss_earth_km = json_all["close_approach_data"][0]["miss_distance"]["kilometers"]
        asteroid_dangerous = json_all["is_potentially_hazardous_asteroid"]

        results_combined = [asteroid_ID, asteroid_name, asteroid_diameter_min, asteroid_diameter_max, asteroid_approach_time, asteroid_kmh, round(float(asteroid_miss_earth_km)), asteroid_dangerous]


        list2.append(results_combined)

        asteroid_underscore = asteroid_name.replace(" ", "_")

        list_asteroid_names.append(asteroid_underscore)

        

        loop_iteration += 1
        print(f"{loop_iteration}. {asteroid_name}\n DIAMETER MIN: {asteroid_diameter_min} meters\n DIAMETER MAX: {asteroid_diameter_max} meters\n DATE: {asteroid_approach_time}\n SPEED: {asteroid_kmh}kmh\n MISS DISTANCE: {asteroid_miss_earth_km}km\n DANGEROUS: {asteroid_dangerous}\n ID: {asteroid_ID}\n ")

    print(list1)


    for el in json_main["near_earth_objects"][f"{end_date}"]:
        json_object = json.dumps(el, indent = 4)
        json_all = json.loads(json_object)

        asteroid_ID = json_all["id"]
        asteroid_name = json_all["name"]
        asteroid_diameter_min = json_all["estimated_diameter"]["meters"]["estimated_diameter_min"]
        asteroid_diameter_max = json_all["estimated_diameter"]["meters"]["estimated_diameter_max"]
        asteroid_approach_time = json_all["close_approach_data"][0]["close_approach_date_full"]
        asteroid_kmh = json_all["close_approach_data"][0]["relative_velocity"]["kilometers_per_hour"]
        asteroid_miss_earth_km = json_all["close_approach_data"][0]["miss_distance"]["kilometers"]
        asteroid_dangerous = json_all["is_potentially_hazardous_asteroid"]

        results_combined = [asteroid_ID, asteroid_name, asteroid_diameter_min, asteroid_diameter_max, asteroid_approach_time, asteroid_kmh, round(float(asteroid_miss_earth_km)), asteroid_dangerous]


        list2.append(results_combined)

        

        loop_iteration += 1
        print(f"{loop_iteration}. {asteroid_name}\n DIAMETER MIN: {asteroid_diameter_min} meters\n DIAMETER MAX: {asteroid_diameter_max} meters\n DATE: {asteroid_approach_time}\n SPEED: {asteroid_kmh}kmh\n MISS DISTANCE: {asteroid_miss_earth_km}km\n DANGEROUS: {asteroid_dangerous}\n ID: {asteroid_ID}\n ")

    print(list1)
    
    return list2

