from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.serializers import TokenVerifySerializer
from rest_framework.exceptions import AuthenticationFailed


class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        token = request.COOKIES.get('access_token')
        if not token:
            return None

        serializer = TokenVerifySerializer(data={'token': token})
        try:
            serializer.is_valid(raise_exception=True)
        except InvalidToken:
            raise AuthenticationFailed('Invalid token')

        validated_token = self.get_validated_token(token)
        return self.get_user(validated_token), validated_token
