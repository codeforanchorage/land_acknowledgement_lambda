import pytest

class Response:
    def __init__(self, data, message, status_code):
        self.data = data
        self.status = status_code
        self.reason = message

    def json(self):
        return self.data

@pytest.fixture()
def FakeResp():
    def _make_respsonse(data, message, status_code):
        return Response(data, message, status_code)
    return _make_respsonse

@pytest.fixture()
def response_404(FakeResp):
    return FakeResp(b'Not Found', 'Not Found', 404)
