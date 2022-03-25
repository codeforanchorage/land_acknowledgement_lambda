import json
from unittest.mock import patch

import pytest
from chalicelib.native_land import native_land_from_point
from chalicelib.errors import APIError

@pytest.fixture
def empyt_result(FakeResp):
     return FakeResp(b"[]", 'OK', 200)


@pytest.fixture
def good_result(FakeResp):
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

@patch('chalicelib.geocode.session.request')
def test_good_location(session, good_result):
    '''It should return a list of dictionaries with the native lands Names'''
    session.return_value = good_result
    result = native_land_from_point(42.553080,-86.473389)
    assert [r['Name'] for r in result] == ["Peoria", "Bodwéwadmi (Potawatomi)"]


@patch('chalicelib.geocode.session.request')
def test_404_location(session, response_404):
    '''It should raise if we get a 404 from api'''
    session.return_value = response_404
    with pytest.raises(APIError) as excinfo:
        native_land_from_point(42.553080,-86.473389)


@patch('chalicelib.geocode.session.request')
def test_empty(session, empyt_result):
    '''It should return an empty list from an emptry response'''
    session.return_value = empyt_result
    assert native_land_from_point(42.553080,-86.473389) == []
