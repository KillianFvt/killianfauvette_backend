from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from cookie_token.auth_class import CookieJWTAuthentication


class Root(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request) -> Response:
        user = request.user
        content = {
            'message': 'Killian Fauvette API',
            'user': {
                'is_authenticated': user.is_authenticated,
                'username': user.username,
                'email': user.email if user.is_authenticated else None,
            },
            'endpoints': [
                '/api/token/',
                '/api/token/refresh/',
                '/api/jwt-test/',
            ],
        }
        return Response(content)


class Home(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request) -> Response:
        content = {
            'user': str(request.user),
            'request': request.data,
            'token': request.COOKIES.get('access_token'),
            'refresh': request.COOKIES.get('refresh_token'),
        }
        return Response(content)

    def post(self, request) -> Response:
        content = {
            'message': 'Post request received',
            'data': request.data
        }
        return Response(content)
