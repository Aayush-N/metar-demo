from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (
		HTTP_200_OK,
	)


class StatusCheck(APIView):
    """
    Returns a response to ensure the system is working fine
    """

    def get(self, request, format=None):
        """
        Return a health check response.
        """
        response_data = {'data': 'pong'}
        return Response(response_data, status=HTTP_200_OK)