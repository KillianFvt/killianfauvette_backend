from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


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
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request) -> Response:
        content = {
            'user': str(request.user),
            'token': str(request.auth)
        }
        return Response(content)

    def post(self, request) -> Response:
        content = {
            'message': 'Post request received',
            'data': request.data
        }
        return Response(content)
