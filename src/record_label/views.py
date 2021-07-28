import requests

from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .utils import restructure_data


@api_view()
def RecordLabelListView(request):
    """
    This view does 3 things:
        1) fetches Festival data from the data API
        2) restructures the data in the required format
        3) returns a HTTP Response (including gracefully handling API errors)

    """

    # Fetch Festival data from data API
    try:
        api_response = requests.get(f"{settings.DATA_API_BASE_URL}/api/v1/festivals")

        # Gracefully handle API error if not a 200 response
        if api_response.status_code != 200:
            return Response(api_response, status=api_response.status_code)

    except requests.exceptions.HTTPError as e:
        # Handle uncaught exception
        return Response({"error": "HTTPError"}, status=400)

    # Restructure the data
    data = api_response.json()

    return_data = restructure_data(data)

    return Response(return_data, status=200)
