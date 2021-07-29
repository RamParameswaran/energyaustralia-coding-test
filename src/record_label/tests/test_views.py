import pytest
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
        resp = RecordLabelListView.as_view()(request)

        assert resp.status_code == 400

    def test_API_429_status_is_gracefully_passed_forward(self, mock_api_request):
        mock_api_request.return_value = mock_response(429)

        request = self.factory.get("/")
        resp = RecordLabelListView.as_view()(request)

        assert resp.status_code == 429


@patch(
    "requests.get",
)
class TestRecordLabelListView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @pytest.mark.django_db
    def test_view_success(self, mock_api_request):
        # Tests a success case using sample data.

        api_data = [
            {
                "name": "Alpha Festival",
                "bands": [
                    {"name": "Band A", "recordLabel": "Record Label 2"},
                ],
            },
            {
                "name": "Beta Festival",
                "bands": [
                    {"name": "Band A", "recordLabel": "Record Label 2"},
                ],
            },
            {
                "name": "Omega Festival",
                "bands": [
                    {"name": "Band X", "recordLabel": "Record Label 1"},
                ],
            },
        ]
        mock_api_request.return_value = mock_response(200, api_data)

        request = self.factory.get("/")
        resp = RecordLabelListView.as_view()(request)

        assert resp.status_code == 200
        assert resp.data == [
            {
                "label": "Record Label 1",
                "bands": [
                    {"name": "Band X", "festivals": [{"name": "Omega Festival"}]}
                ],
            },
            {
                "label": "Record Label 2",
                "bands": [
                    {
                        "name": "Band A",
                        "festivals": [
                            {"name": "Alpha Festival"},
                            {"name": "Beta Festival"},
                        ],
                    }
                ],
            },
        ]

    @pytest.mark.django_db
    def test_view_success_with_missing_data(self, mock_api_request):
        # Tests that the View function handles missing data, and preserves order
        # correctly.

        api_data = [
            {
                "name": "Alpha Festival",
                "bands": [
                    {"name": "Band A"},
                ],
            },
            {
                "name": "Beta Festival",
                "bands": [
                    {"name": "Band A", "recordLabel": "Record Label 2"},
                ],
            },
            {
                "name": "Omega Festival",
                "bands": [
                    {"name": "Band X", "recordLabel": "Record Label 1"},
                ],
            },
        ]
        mock_api_request.return_value = mock_response(200, api_data)

        request = self.factory.get("/")
        resp = RecordLabelListView.as_view()(request)

        assert resp.status_code == 200
        assert resp.data == [
            {
                "label": None,
                "bands": [
                    {
                        "name": "Band A",
                        "festivals": [
                            {"name": "Alpha Festival"},
                        ],
                    }
                ],
            },
            {
                "label": "Record Label 1",
                "bands": [
                    {"name": "Band X", "festivals": [{"name": "Omega Festival"}]}
                ],
            },
            {
                "label": "Record Label 2",
                "bands": [
                    {
                        "name": "Band A",
                        "festivals": [
                            {"name": "Beta Festival"},
                        ],
                    }
                ],
            },
        ]
