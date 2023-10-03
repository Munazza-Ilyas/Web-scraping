import datetime
from dateutil.parser import isoparse

def extract_timeseriesx(raw_data):
    """Returns a list of all timeseries (as dict),
    given the raw data as dict."""
    if "value" in raw_data and "timeSeries" in raw_data["value"]:
         timeseries_list = raw_data["value"]["timeSeries"]
         timeseries_dicts = []
         for timeseries in timeseries_list:
            timeseries_dict = {
                "sourceInfo" : timeseries["sourceInfo"],
                "variable" : timeseries["variable"],
                "values": timeseries["values"],
                "name":timeseries["name"],
            }
            timeseries_dicts.append(timeseries_dict)
            
    return timeseries_dicts

def extract_metadata_from_timeseries(timeseries):
    """Takes a single timeseries as dict and extracts the metadata as a dict
    with the keys "site_name", "latitude", "longitude" and "variable_name".
    The values for "latitude" and "longitude" are floats."""

    metadata = {
    "site_name" : timeseries["sourceInfo"]["siteName"],
    "latitude" : float(timeseries["sourceInfo"]["geoLocation"]["geogLocation"]["latitude"]),
    "longitude" : float(timeseries["sourceInfo"]["geoLocation"]["geogLocation"]["longitude"]),
    "variable_name" : timeseries["variable"]["variableName"],
    }  
    return metadata


def extract_values_from_timerseries(timeseries):
    """Takes a single timeseries as dict and extracts the values as a list of dictionaries
    with keys "datetime" and "value".
    The "datetime" values should be of type datetime.datetime.
    The "value" value should be a float.
    """

    # note: timeseries["values"] is a list.
    # Its unclear why its a list,
    # because each element of it has a "value" key with a list as its values.
    # So, it can already accommodate multiple values.
    # Also, from spot checking timeseries["values"] appears to be of length 1.
    # So, use only the first element of the list.
    
    
    values = timeseries["values"][0]["value"]

    extracted_values = []

    for value_entry in values:
        datetime_obj = isoparse(value_entry["dateTime"])
        value_dict = {
            "datetime": datetime_obj,
            "value": float(value_entry["value"]),
        }

        extracted_values.append(value_dict)

    return extracted_values


def extract_data_from_timeseries(timeseries):
    """Extracts all of the data from a timeseries
    by taking each row (a dict) of the values (values is a list of dicts)
    and adding the metadata (a dict).
    Returns a list of dicts."""

    metadata = extract_metadata_from_timeseries(timeseries)
    values = extract_values_from_timerseries(timeseries)
    data_list = []

    for value_entry in values:
        data_entry = {**metadata, **value_entry}
        data_list.append(data_entry)
    return data_list


def extract_data(data):

    timeseriesx = extract_timeseriesx(data)
    combined_data = []

    for timeseries in timeseriesx:
        data_each_timeseries = extract_data_from_timeseries(timeseries)
        l = len(data_each_timeseries)
        if l > 0:
            for m in range(0,l):
                combined_data.append(data_each_timeseries[m])
    return combined_data


if __name__ == "__main__":

    example_timeseries = {
        "sourceInfo": {
            "siteName": "KH-65-40-707 (Galveston)",
            "siteCode": [
                {"value": "292338095063601", "network": "NWIS", "agencyCode": "USGS"}
            ],
            "timeZoneInfo": {
                "defaultTimeZone": {"zoneOffset": "-06:00", "zoneAbbreviation": "CST"},
                "daylightSavingsTimeZone": {
                    "zoneOffset": "-05:00",
                    "zoneAbbreviation": "CDT",
                },
                "siteUsesDaylightSavingsTime": True,
            },
            "geoLocation": {
                "geogLocation": {
                    "srs": "EPSG:4326",
                    "latitude": 29.39416667,
                    "longitude": -95.1102778,
                },
                "localSiteXY": [],
            },
            "note": [],
            "siteType": [],
            "siteProperty": [
                {"value": "GW", "name": "siteTypeCd"},
                {"value": "12040204", "name": "hucCd"},
                {"value": "48", "name": "stateCd"},
                {"value": "48167", "name": "countyCd"},
            ],
        },
        "variable": {
            "variableCode": [
                {
                    "value": "62610",
                    "network": "NWIS",
                    "vocabulary": "NWIS:UnitValues",
                    "variableID": 51413516,
                    "default": True,
                }
            ],
            "variableName": "Groundwater level above NGVD 1929, feet",
            "variableDescription": "Groundwater level above NGVD 1929, feet",
            "valueType": "Derived Value",
            "unit": {"unitCode": "ft"},
            "options": {"option": [{"name": "Statistic", "optionCode": "00000"}]},
            "note": [],
            "noDataValue": -999999.0,
            "variableProperty": [],
            "oid": "51413516",
        },
        "values": [
            {
                "value": [
                    {
                        "value": "-64.58",
                        "qualifiers": ["A", "1"],
                        "dateTime": "2022-06-28T13:16:00.000",
                    },
                    {
                        "value": "-65.87",
                        "qualifiers": ["P", "1"],
                        "dateTime": "2022-09-14T14:01:00.000",
                    },
                ],
                "qualifier": [
                    {
                        "qualifierCode": "1",
                        "qualifierDescription": "Static",
                        "qualifierID": 0,
                        "network": "NWIS",
                        "vocabulary": "uv_rmk_cd",
                    },
                    {
                        "qualifierCode": "A",
                        "qualifierDescription": "Approved for publication -- Processing and review completed.",
                        "qualifierID": 1,
                        "network": "NWIS",
                        "vocabulary": "uv_rmk_cd",
                    },
                    {
                        "qualifierCode": "P",
                        "qualifierDescription": "Provisional data subject to revision.",
                        "qualifierID": 2,
                        "network": "NWIS",
                        "vocabulary": "uv_rmk_cd",
                    },
                ],
                "qualityControlLevel": [],
                "method": [{"methodID": 1}],
                "source": [],
                "offset": [],
                "sample": [],
                "censorCode": [],
            }
        ],
        "name": "USGS:292338095063601:62610:00000",
    }

    expected_metadata = {
        "site_name": "KH-65-40-707 (Galveston)",
        "latitude": 29.39416667,
        "longitude": -95.1102778,
        "variable_name": "Groundwater level above NGVD 1929, feet",
    }

    expected_values = [
        {"value": -64.58, "datetime": datetime.datetime(2022, 6, 28, 13, 16)},
        {"value": -65.87, "datetime": datetime.datetime(2022, 9, 14, 14, 1)},
    ]

    expected_data = [
        {
            "value": -64.58,
            "datetime": datetime.datetime(2022, 6, 28, 13, 16),
            "site_name": "KH-65-40-707 (Galveston)",
            "latitude": 29.39416667,
            "longitude": -95.1102778,
            "variable_name": "Groundwater level above NGVD 1929, feet",
        },
        {
            "value": -65.87,
            "datetime": datetime.datetime(2022, 9, 14, 14, 1),
            "site_name": "KH-65-40-707 (Galveston)",
            "latitude": 29.39416667,
            "longitude": -95.1102778,
            "variable_name": "Groundwater level above NGVD 1929, feet",
        },
    ]

    assert extract_metadata_from_timeseries(example_timeseries) == expected_metadata

    assert extract_values_from_timerseries(example_timeseries) == expected_values

    assert extract_data_from_timeseries(example_timeseries) == expected_data
