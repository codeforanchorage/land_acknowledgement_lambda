import json

import pytest


class Response:
    def __init__(self, data, message, status_code):
        self.data = data
        self.status = status_code
        self.reason = message

    def json(self):
        return self.data

@pytest.fixture()
def FakeResp():
    def _make_respsonse(data, message, status_code):
        return Response(data, message, status_code)
    return _make_respsonse

@pytest.fixture()
def response_404(FakeResp):
    return FakeResp(b'Not Found', 'Not Found', 404)

@pytest.fixture
def good_zip_location(FakeResp):
    d = {
       "type": "FeatureCollection",
        "query": ["60614"],
        "features": [{
            "id": "postcode.14189074987591320",
            "type": "Feature",
            "place_type": ["postcode"],
            "relevance": 1,
            "properties": {},
            "text": "60614",
            "place_name": "Chicago, Illinois 60614, United States",
            "bbox": [-87.678274, 41.910784178, -87.620164014, 41.93498],
            "center": [-87.65, 41.93],
            "geometry": {
                "type": "Point",
                "coordinates": [-87.65, 41.93]
            },
            "context": [
                {
                    "id": "place.9607189446701850",
                    "wikidata": "Q1297",
                    "text": "Chicago"
                },
            ]
        }]
    }
    return FakeResp(json.dumps(d).encode('utf-8'), 'OK', 200)

@pytest.fixture
def good_geo_location(FakeResp):
    d = {
        'type': 'FeatureCollection',
        'query': ['chicago', 'il'],
        'features': [
            {
                'id': 'place.19268916718032980',
                'type': 'Feature',
                'place_type': ['place'],
                'relevance': .9,
                'text': 'Seattle',
                'place_name': 'Seattle, Washington, United States',
                'bbox': [-122.435900266, 47.350685958, -122.218864003, 47.778803038],
                'center': [-122.3301, 47.6038],
                'geometry': {'type': 'Point', 'coordinates': [-122.3301, 47.6038]},
                "context": [
                    {
                        "id": "district.8754923997749290",
                        "wikidata": "Q108418",
                        "text": "Cook County"
                    }
                ],
            },
            {
                'id': 'poi.472446423802',
                'type': 'Feature',
                'place_type': ['poi'],
                'relevance': 1,
                'text': 'Chicago',
                'place_name': 'Chicago Midway International Airport (MDW), 5700 S Cicero Ave, Chicago, Illinois 60638, United States',
                'center': [-87.747394, 41.786872],
                'geometry': {'coordinates': [-87.747394, 41.786872], 'type': 'Point'},
                "context": [
                    {
                        "id": "district.8754923997749290",
                        "wikidata": "Q108418",
                        "text": "Cook County"
                    }
                ],
            },
            {
                'id': 'place.19268916718032980',
                'type': 'Feature',
                'place_type': ['place'],
                'relevance': 1,
                "text": "Chicago",
                "place_name": "Chicago, Illinois, United States",
                "bbox": [-87.931085223, 41.625740009, -87.507792006, 42.023137],
                "center": [-87.6244, 41.8756],
                'geometry': {'type': 'Point', 'coordinates': [-149.8949, 61.2163]},
                "context": [
                    {
                        "id": "district.8754923997749290",
                        "wikidata": "Q108418",
                        "text": "Cook County"
                    }
                ],
            },
       ]
    }
    return FakeResp(json.dumps(d).encode('utf-8'), 'OK', 200)

@pytest.fixture
def good_native_land_result(FakeResp):
    resp = [
        {
            "type": "Feature",
            "properties": {
                "Name": "Peoria",
                "FrenchDescription": "https://native-land.ca/maps/territories/peoria/",
                "FrenchName": "Peoria",
                "Slug": "peoria",
                "color": "#D811BB",
                "description": "https://native-land.ca/maps/territories/peoria/"
            },
            "geometry": {
                "coordinates": [
                    [
                        [
                            -90.54696,
                            41.54317
                        ],
                    ]
                ],
                "type": "Polygon"
            },
            "id": "155d688cb2e7d81c11de3beee6b60b4a"
        },
        {
            "type": "Feature",
            "properties": {
                "Name": "Bodwéwadmi (Potawatomi)",
                "FrenchName": "Bodwéwadmi (Potawatomi)",
                "Slug": "potawatomi",
                "description": "https://native-land.ca/maps/territories/bodwewadmi-potawatomi/",
                "FrenchDescription": "https://native-land.ca/maps/territories/bodwewadmi-potawatomi/",
                "color": "#167925"
            },
            "geometry": {
                "coordinates": [
                    [
                        [
                            -87.099609,
                            42.956423
                        ],
                    ]
                ],
                "type": "Polygon"
            },
            "id": "82d1b98e51e24cad54babbf2d4d34c52"
        }
    ]
    return FakeResp(json.dumps(resp).encode('utf-8'), 'OK', 200)
