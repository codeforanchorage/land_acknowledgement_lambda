from unittest.mock import patch, MagicMock
import pytest
from chalice.test import Client
from app import app

def test_index():
    '''It should post help text with empty qeury'''
    with Client(app) as client:
        response = client.http.get('/')
        default_response = "Hello. Please tell me the town and state you are in. For example, 'Anchorage, AK'"
        assert response.body.decode() == default_response


@patch('chalicelib.http.session.request')
def test_get_location(request, good_geo_location, good_native_land_result):
    '''It should respond with text that includes both the queried location and native lands'''
    query = 'some%20query'
    with Client(app) as client:
        request.side_effect =  [good_geo_location, good_native_land_result]
        response = client.http.get('/'+query)
        assert response.body.decode() == 'In Chicago you are on Peoria and Bodwéwadmi (Potawatomi) land.'


@patch('chalicelib.http.session.request')
def test_get_zipcode(request, good_zip_location, good_native_land_result):
    '''It should respond with text that includes both the zip code and native lands'''
    query = 'some_zip'
    with Client(app) as client:
        request.side_effect =  [good_zip_location, good_native_land_result]
        response = client.http.get('/'+query)
        assert response.body.decode() == 'In the area of 60614 you are on Peoria and Bodwéwadmi (Potawatomi) land.'


@patch('chalicelib.http.session.request')
@patch('chalicelib.responses.native_land_from_point')
def test_queries_coords_( native_land_from_point, request, good_geo_location):
    '''It should use the coordinates from the geolcation to look for native lands'''
    query = 'some%20query'
    with Client(app) as client:
        request.side_effect =  [good_geo_location]
        response = client.http.get('/'+query)
        native_land_from_point.assert_called_with(-87.6244,41.8756)
