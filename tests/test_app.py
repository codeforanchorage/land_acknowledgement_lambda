from unittest.mock import patch, MagicMock
import pytest
from chalice.test import Client
from app import app

def test_index():
    with Client(app) as client:
        response = client.http.get('/')
        default_response = "Hello. Please tell me the town and state you are in. For example, 'Anchorage, AK'"
        assert response.body.decode() == default_response


#@patch('chalicelib.geocode.session.request')
@patch('chalicelib.http.session.request')
def test_get_location(request, good_geo_location, good_native_land_result):
    query = 'Anchorage%20ak'
    with Client(app) as client:
        request.side_effect =  [good_geo_location, good_native_land_result]
        #native_land_request.return_value = good_native_land_result
        response = client.http.get('/'+query)
        assert response.body == b'In Chicago you are on Peoria and Bodw\xc3\xa9wadmi (Potawatomi) land.'
