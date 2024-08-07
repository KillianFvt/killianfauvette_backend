from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from cookie_token.serializers import CookieTokenRefreshSerializer


class CookieTokenObtainPairView(TokenObtainPairView):
    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get('refresh'):
            cookie_max_age = 3600 * 24 * 31  # 31 days
            response.set_cookie(
                'refresh_token',
                response.data['refresh'],
                max_age=cookie_max_age,
                httponly=True,
                secure=True,
                samesite='None'
            )
            del response.data['refresh']

        if response.data.get('access'):
            access_token_expiry = 3600  # 1 hour
            response.set_cookie(
                'access_token',
                response.data['access'],
                max_age=access_token_expiry,
                httponly=True,
                secure=True,
                samesite='None'
            )
            del response.data['access']

        return super().finalize_response(request, response, *args, **kwargs)


class CookieTokenRefreshView(TokenRefreshView):
    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get('refresh'):
            cookie_max_age = 3600 * 24 * 31  # 31 days
            response.set_cookie(
                'refresh_token',
                response.data['refresh'],
                max_age=cookie_max_age,
                httponly=True
            )
            del response.data['refresh']

        if response.data.get('access'):
            access_token_expiry = 3600  # 1 hour
            response.set_cookie(
                'access_token',
                response.data['access'],
                max_age=access_token_expiry,
                httponly=True
            )
            del response.data['access']

        return super().finalize_response(request, response, *args, **kwargs)

    serializer_class = CookieTokenRefreshSerializer
