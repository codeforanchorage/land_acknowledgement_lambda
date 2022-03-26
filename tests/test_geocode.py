from unittest.mock import patch
import pytest
import json

from chalicelib.geocode import geolocate
from chalicelib.errors import LocationNotFound


@pytest.fixture
def empty_geo_locations(FakeResp):
    d = {
        'type': 'FeatureCollection',
        'query': ['blah'],
        'features': []
    }
    return FakeResp(json.dumps(d).encode('utf-8'), 'OK', 200)




@patch('chalicelib.geocode.session.request')
def test_404_location(session, response_404):
    '''It should raise location not found error on 404 from api'''
    session.return_value = response_404
    with pytest.raises(LocationNotFound) as excinfo:
        result = geolocate("some place")


@patch('chalicelib.geocode.session.request')
def test_best_location(session, good_geo_location):
    '''It should favor places over other types of locations and pick highest relevance'''
    session.return_value = good_geo_location
    result = geolocate("some place")
    assert result['text'] == 'Chicago'
    assert result['place_type'] == ['place']


@patch('chalicelib.geocode.session.request')
def test_no_location(session, empty_geo_locations):
    '''It should favore places over other types of locations and pick highest relevance'''
    session.return_value = empty_geo_locations
    with pytest.raises(LocationNotFound) as excinfo:
        result = geolocate("blah")
    