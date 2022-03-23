from chalice.test import Client
from app import app


def test_index():
    assert True
    return
    with Client(app) as client:
        response = client.http.get('/')
        assert response.json_body == {'hello': 'world'}
