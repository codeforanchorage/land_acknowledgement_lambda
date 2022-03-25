from unittest.mock import patch
import pytest
import json

from chalicelib.geocode import geolocate
from chalicelib.errors import LocationNotFound

@pytest.fixture()
def response_404(FakeResp):
    return FakeResp(b'Not Found', 'Not Found', 404)


@pytest.fixture
def empty_geo_locations(FakeResp):
    d = {
        'type': 'FeatureCollection',
        'query': ['blah'],
        'features': []
    }
    return FakeResp(json.dumps(d).encode('utf-8'), 'OK', 200)


@pytest.fixture
def good_geo_location(FakeResp):
    d = {
        'type': 'FeatureCollection',
        'query': ['anchorage', 'ak'],
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
            },  
            {
                'id': 'place.19268916718032980',
                'type': 'Feature',
                'place_type': ['place'],
                'relevance': 1,
                'text': 'Anchorage',
                'place_name': 'Anchorage, Alaska, United States',
                'bbox': [-159.516899997364, 55.8944109861981, -141.00268595324, 70.6124380154738],
                'center': [-149.8949, 61.2163],
                'geometry': {'type': 'Point', 'coordinates': [-149.8949, 61.2163]},   
            }
       ]
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
    assert result['text'] == 'Anchorage'
    assert result['place_type'] == ['place']


@patch('chalicelib.geocode.session.request')
def test_no_location(session, empty_geo_locations):
    '''It should favore places over other types of locations and pick highest relevance'''
    session.return_value = empty_geo_locations
    with pytest.raises(LocationNotFound) as excinfo:
        result = geolocate("blah")
    