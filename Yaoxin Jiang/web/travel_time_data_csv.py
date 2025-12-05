import math
import os
import pandas as pd
import numpy as np
df = pd.read_csv('1101-modified+RMP-2025-sp.csv')
import os
import googlemaps
#from dotenv import load_dotenv
from typing import List, Union, Optional
API_KEY = "AIzaSyDKfrpFNE6saT16tngJPH4MQTAgQNk6zN8"
gmaps = googlemaps.Client(key=API_KEY)


print("Hello World")

#this function takes two locations and return walking time between them
def get_walking_time(origin, destination):
    try:
        response = gmaps.distance_matrix( #type: ignore

            origins=[origin],
            destinations=[destination],
            mode="walking",
            departure_time="now"
        )

        #extract walking time from the response
        info = response['rows'][0]['elements'][0]
        if info['status'] == 'OK':
            seconds = info['duration']['value'] #get time in second
            minutes = seconds / 60 #convert to minutes
            return round(minutes, 2) #round to 2dp
        else :
            return None
    except Exception as e:
        print(f"Error while calculating walking time from {origin} to {destination}: {e}")
        return None

#print(get_walking_time("hendrick House, IL", "Illinois Street Residence Halls, IL"))


locations = []
for i in range(0, 14149):
    if df.loc[i, 'Building'] not in locations:
        locations.append(df.loc[i, 'Building'])

print(len(locations))


