import json
from unittest.mock import patch

import pytest
from chalicelib.native_land import native_land_from_point
from chalicelib.errors import APIError

@pytest.fixture
def empyt_result(FakeResp):
     return FakeResp(b"[]", 'OK', 200)


@patch('chalicelib.geocode.session.request')
def test_good_location(session, good_native_land_result):
    '''It should return a list of dictionaries with the native lands Names'''
    session.return_value = good_native_land_result
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
