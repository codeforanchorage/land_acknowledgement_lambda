from unittest.mock import patch

import pytest

from chalicelib.errors import APIError
from chalicelib.native_land import native_land_from_point


@pytest.fixture
def empty_result(FakeResp):
    return FakeResp(b"[]", 'OK', 200)


@patch('chalicelib.geocode.session.request')
def test_good_location(mock_get, good_native_land_result):
    '''It should return a list of dictionaries with the native lands Names'''
    mock_get.return_value = good_native_land_result
    result = native_land_from_point(42.553080, -86.473389)
    assert [r['Name'] for r in result] == ["Peoria", "Bodwéwadmi (Potawatomi)"]


@patch('chalicelib.geocode.session.request')
def test_404_location(mock_get, response_404):
    '''It should raise if we get a 404 from api'''
    mock_get.return_value = response_404
    with pytest.raises(APIError):
        native_land_from_point(42.553080, -86.473389)


@patch('chalicelib.geocode.session.request')
def test_empty(mock_get, empty_result):
    '''It should return an empty list from an emptry response'''
    mock_get.return_value = empty_result
    assert native_land_from_point(42.553080, -86.473389) == []
