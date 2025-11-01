## Time organizing program

import json
import os

DATA_FILE = "data.json"

def load_data():
    # Load datafile / create it if it doesnt exist
    if not os.path.exists(DATA_FILE):
        data = {"timetable": {}, "progress": {}}
        save_data(data)
        return data
    with open(DATA_FILE, "r") as df:
        return json.load(df)
    
def save_data(data):
    # Saving data
    with open(DATA_FILE, "w") as df:
        json.dump(data, f, indent=4)