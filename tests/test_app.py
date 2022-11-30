from unittest.mock import patch
from xml.dom import minidom

from chalice.test import Client

from app import app


def get_message_from_xml(xml_string):
    '''Just a little help to deal with twilio's xml format'''
    xmldoc = minidom.parseString(xml_string)
    itemlist = xmldoc.getElementsByTagName('Message')
    return itemlist[0].firstChild.data


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
        request.side_effect = [good_geo_location, good_native_land_result]
        response = client.http.get('/'+query)
        assert response.body.decode() == 'In Chicago you are on Peoria and Bodwéwadmi (Potawatomi) land.'


def test_get_short_location():
    '''Short queries should get an error message'''
    queries = [
        'a',
        'ab',
        'XX',
    ]
    with Client(app) as client:
        for query in queries:
            response = client.http.get('/'+query)
            assert response.body.decode() == "Hmm, that seems a little vague. Try sending a city and state such as 'Anchorage, AK'"


@patch('chalicelib.http.session.request')
def test_post_location(request, good_geo_location, good_native_land_result):
    '''It should respond with twiML that includes both the queried location and native lands'''

    with Client(app) as client:
        request.side_effect = [good_geo_location, good_native_land_result]

        response = client.http.post(
            '/',
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            body=b'Body=Chicago, il'
        )

        result_string = get_message_from_xml(response.body.decode())
        assert result_string == '\n'.join(
            [
                'In Chicago you are on Peoria and Bodwéwadmi (Potawatomi) land.',
                'More info: https://land.codeforanchorage.org',
            ]
        )


@patch('chalicelib.http.session.request')
def test_get_zipcode(request, good_zip_location, good_native_land_result):
    '''It should respond with text that includes both the zip code and native lands'''
    query = 'some_zip'
    with Client(app) as client:
        request.side_effect = [good_zip_location, good_native_land_result]
        response = client.http.get('/'+query)
        assert response.body.decode() == 'In the area of 60614 you are on Peoria and Bodwéwadmi (Potawatomi) land.'


@patch('chalicelib.http.session.request')
@patch('chalicelib.responses.native_land_from_point')
def test_queries_coords_(native_land_from_point, request, good_geo_location):
    '''It should use the coordinates from the geolcation to look for native lands'''
    query = 'some%20query'
    with Client(app) as client:
        request.side_effect = [good_geo_location]
        client.http.get('/'+query)
        native_land_from_point.assert_called_with(-87.6244, 41.8756)
