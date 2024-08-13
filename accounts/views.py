from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from accounts.serializers import UserSerializer
from cookie_token.auth_class import CookieJWTAuthentication


class UserViewSet(viewsets.ModelViewSet):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get(self, request) -> Response:
        user = request.user
        content = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }

        return Response(content)

    @action(detail=False, methods=['get'])
    def search_users(self, request) -> Response:
        query = request.query_params.get('query')

        if not query:
            return Response({'error': 'query parameter is required'}, status=400)

        users = (
            User.objects.filter(username__icontains=query) |
            User.objects.filter(email__icontains=query) |
            User.objects.filter(first_name__icontains=query) |
            User.objects.filter(last_name__icontains=query) |
            User.objects.filter(id__icontains=query)
        )

        users = users.distinct()
        users = users[:10]
        return Response([{
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        } for user in users])
