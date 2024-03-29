import json
from unittest.mock import patch

import pytest

from chalicelib.errors import LocationNotFound
from chalicelib.geocode import geolocate


@pytest.fixture
def empty_geo_locations(FakeResp):
    d = {
        'type': 'FeatureCollection',
        'query': ['blah'],
        'features': []
    }
    return FakeResp(json.dumps(d).encode('utf-8'), 'OK', 200)


@patch('chalicelib.geocode.session.request')
def test_404_location(mock_get, response_404):
    '''It should raise location not found error on 404 from api'''
    mock_get.return_value = response_404
    with pytest.raises(LocationNotFound):
        geolocate("some place")


@patch('chalicelib.geocode.session.request')
def test_best_location(mock_get, good_geo_location):
    '''It should favor places over other types of locations and pick highest relevance'''
    mock_get.return_value = good_geo_location
    result = geolocate("some place")
    assert result['text'] == 'Chicago'
    assert result['place_type'] == ['place']


@patch('chalicelib.geocode.session.request')
def test_no_location(mock_get, empty_geo_locations):
    '''It should favor places over other types of locations and pick highest relevance'''
    mock_get.return_value = empty_geo_locations
    with pytest.raises(LocationNotFound):
        geolocate("blah")
