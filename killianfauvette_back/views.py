from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


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
