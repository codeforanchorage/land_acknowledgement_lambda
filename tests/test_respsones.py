import pytest

from chalicelib.responses import GenericResponse

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

def test_land_string_more_than_two(lands_list):
    '''It should make a string with names seperated by commas with a final "and"'''
    r = GenericResponse('some query', 'somelocation')
    assert r.land_string(lands_list) == "Peoria, Bodwéwadmi (Potawatomi), and Mvskoke (Muscogee)"

def test_land_string_two(lands_list):
    '''It should make a string with names seperated by "and"'''
    r = GenericResponse('some query', 'somelocation')
    assert r.land_string(lands_list[:2]) == "Peoria and Bodwéwadmi (Potawatomi)"

def test_land_string_one(lands_list):
    '''It should make a string with names seperated by "and"'''
    r = GenericResponse('some query', 'somelocation')
    assert r.land_string(lands_list[:1]) == "Peoria"