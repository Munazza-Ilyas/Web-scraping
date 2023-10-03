import os
import csv
import json
import requests

from clean_data import extract_data

BASE_DIR = "artifacts"
FILENAME = "results.csv"
CSV_PATH = os.path.join(BASE_DIR,FILENAME)
os.makedirs(BASE_DIR, exist_ok=True)

def request_raw_data():
    """Requests the groundwater levels
    for summer of 2022 (Jun 6th to Sept 22)
    for Texas
    in a JSON format.
    Allows gzip compression in transit.
    Returns a dictionary representing the JSON response.
    """
    base_url = "https://waterservices.usgs.gov/nwis/gwlevels"
    headers = {"Accept-Encoding":"gzip",}
    params = {"format":"json", "stateCd":"TX","startDT":"2022-06-21","endDT":"2022-09-22"}
    response= requests.get(base_url,params=params, headers=headers)
    data = response.json()
    return data

raw_data = request_raw_data()
clean_data = extract_data(raw_data)

def sort_data(data):
    """Sort the data lexicographically by "variable_name", "site_name" and then "datetime"."""
    def custom_sort_key(entry):
        return(entry["variable_name"],entry["site_name"],entry["datetime"])
    sorted_data = sorted(data,key=custom_sort_key)
    return sorted_data

sorted_data = sort_data(clean_data)

def write_data_to_csv(data, path):
    """Write the data to the csv.
    The columns should be in the order:
        "variable_name",
        "site_name",
        "datetime",
        "value",
        "longitude",
        "latitude"
    """
    fieldnames = [
        "variable_name",
        "site_name",
        "datetime",
        "value",
        "longitude",
        "latitude",
    ]
    
    with open(path, mode='w+', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        
        writer.writeheader()
        
        for entry in data:
            writer.writerow({
                "variable_name": entry["variable_name"],
                "site_name": entry["site_name"],
                "datetime": entry["datetime"],
                "value": entry["value"],
                "longitude": entry["longitude"],
                "latitude": entry["latitude"],
            })
            
write_data_to_csv(sorted_data,CSV_PATH)
 


if __name__ == "__main__":

    BASE_DIR = "artifacts"
    CSV_PATH = os.path.join(BASE_DIR, "results.csv")

    os.makedirs(BASE_DIR, exist_ok=True)

    raw_data = request_raw_data()
    clean_data = extract_data(raw_data)
    sorted_data = sort_data(clean_data)

    write_data_to_csv(sorted_data, CSV_PATH)
