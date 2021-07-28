import requests

from django.test import RequestFactory, TestCase
from unittest.mock import Mock, patch

from record_label.views import RecordLabelListView


def mock_response(status, data=None):
    r = requests.Response()
    r.status_code = status

    def json_func():
        return data

    r.json = json_func
    return r


@patch(
    "requests.get",
)
class TestRecordLabelListView_ApiRequestHandling(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_API_exception_is_gracefully_passed_forward(self, mock_api_request):
        mock_api_request.side_effect = Mock(side_effect=requests.exceptions.HTTPError())

        request = self.factory.get("/")
        resp = RecordLabelListView(request)

        assert resp.status_code == 400

    def test_API_429_status_is_gracefully_passed_forward(self, mock_api_request):
        mock_api_request.return_value = mock_response(429)

        request = self.factory.get("/")
        resp = RecordLabelListView(request)

        assert resp.status_code == 429
