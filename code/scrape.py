import os
import csv

import requests

from clean_data import extract_data


def request_raw_data():
    """Requests the groundwater levels
    for summer of 2022 (Jun 6th to Sept 22)
    for Texas
    in a JSON format.
    Allows gzip compression in transit.
    Returns a dictionary representing the JSON response.
    """

    return


def sort_data(data):
    """Sort the data lexicographically by "variable_name", "site_name" and then "datetime"."""

    return


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

    return


if __name__ == "__main__":

    BASE_DIR = "artifacts"
    CSV_PATH = os.path.join(BASE_DIR, "results.csv")

    os.makedirs(BASE_DIR, exist_ok=True)

    raw_data = request_raw_data()
    clean_data = extract_data(raw_data)
    sorted_data = sort_data(clean_data)

    write_data_to_csv(sorted_data, CSV_PATH)
