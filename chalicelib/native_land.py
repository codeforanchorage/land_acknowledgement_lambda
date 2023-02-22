import json

from chalicelib.http import session
from chalicelib.errors import APIError


API_BASE = "https://native-land.ca/api/index.php"


def native_land_from_point(lon, lat):
    """lat lon in format: 42.553080,-86.473389"""
    query = {"maps": "territories", "position": f"{lat},{lon}"}
    resp = session.request("GET", API_BASE, fields=query)

    if resp.status != 200:
        raise APIError(resp.reason)
    data = json.loads(resp.data.decode("utf-8"))
    return [d["properties"] for d in data if d["type"] == "Feature"]
