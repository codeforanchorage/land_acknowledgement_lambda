import pytest
from unittest.mock import patch

from chalicelib.responses import LocationResponse

@pytest.fixture
def lands_list():
    return [
        {
            "Name": "Peoria",
            "FrenchDescription": "https://native-land.ca/maps/territories/peoria/",
            "FrenchName": "Peoria",
            "Slug": "peoria",
            "color": "#D811BB",
            "description": "https://native-land.ca/maps/territories/peoria/"
        },
        {
            "Name": "Bodwéwadmi (Potawatomi)",
            "FrenchName": "Bodwéwadmi (Potawatomi)",
            "Slug": "potawatomi",
            "description": "https://native-land.ca/maps/territories/bodwewadmi-potawatomi/",
            "FrenchDescription": "https://native-land.ca/maps/territories/bodwewadmi-potawatomi/",
            "color": "#167925"
        },
        {
            "Name": "Mvskoke (Muscogee)",
            "FrenchName": "Mvskoke (Muscogee)",
            "Slug": "muscogee-creek",
            "description": "https://native-land.ca/maps/territories/muscogee/",
            "FrenchDescription": "https://native-land.ca/maps/territories/muscogee/",
            "color": "#A62288"
        },
]

@patch('chalicelib.responses.native_land_from_point')
def test_land_string_more_than_two(land_point_mock, lands_list):
    '''It should make a string with names seperated by commas with a final "and"'''
    land_point_mock.return_value = lands_list
    someLocation = {"center": [10, 10]}
    r = LocationResponse('some query', someLocation)
    assert r.land_string() == "Peoria, Bodwéwadmi (Potawatomi), and Mvskoke (Muscogee)"

@patch('chalicelib.responses.native_land_from_point')
def test_land_string_two(land_point_mock, lands_list):
    '''It should make a string with names seperated by "and"'''
    land_point_mock.return_value = lands_list[:2]
    someLocation = {"center": [10, 10]}
    r = LocationResponse('some query', someLocation)
    assert r.land_string() == "Peoria and Bodwéwadmi (Potawatomi)"

@patch('chalicelib.responses.native_land_from_point')
def test_land_string_one(land_point_mock, lands_list):
    '''It should make a string with names seperated by "and"'''
    land_point_mock.return_value = lands_list[:1]
    someLocation = {"center": [10, 10]}
    r = LocationResponse('some query', someLocation)
    assert r.land_string() == "Peoria"