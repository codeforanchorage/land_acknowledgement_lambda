import os
import json

from chalicelib.errors import APIError, LocationNotFound, ConfigurationError
from chalicelib.http import session
from chalicelib.get_secret import get_secret


API_BASE = "https://api.mapbox.com/geocoding/v5/mapbox.places/"


def geolocate(raw_str):
    MAPBOX_TOKEN = os.getenv("MAPBOX_TOKEN") or get_secret("MAPBOX_TOKEN")

    if MAPBOX_TOKEN is None:
        raise ConfigurationError(
            "The env MAPBOX_TOKEN is missing from the environment."
        )

    query = {"access_token": MAPBOX_TOKEN, "type": "place"}
    url = API_BASE + raw_str + ".json"
    resp = session.request("GET", url, fields=query)

    if resp.status == 404:
        raise LocationNotFound(raw_str)
    elif resp.status != 200:
        raise APIError(resp.reason)

    data = json.loads(resp.data.decode("utf-8"))
    try:
        return location_from_collection(data)
    except LocationNotFound:
        raise LocationNotFound(raw_str)


def location_from_collection(json_data):
    """
    Returns the best feature from the collection of features
    returned by api. Best is determined by sorting by relevance then type in
    a way that favors places over less desireable results like POI.
    Raises LocationNotFound if the API returns an empty collection.
    """

    priorities = {
        "place": 10,
        "postcode": 10,
        "locality": 9,
        "address": 8,
        "region": 7,
        "country": 6,
        "district": 5,
        "neighborhood": 5,
        "poi": 4,
    }

    features = json_data["features"]
    if len(features) == 0:
        raise LocationNotFound
    return max(
        features,
        key=lambda f: (f["relevance"], priorities.get(f["place_type"][0], 0)),
    )
