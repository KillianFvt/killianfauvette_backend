from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import Test, Root

urlpatterns = [
    path('', Root.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('token/', include('cookie_token.urls')),
    path('tokenold/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('tokenold/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('jwt-test/', Test.as_view(), name='jwt-test'),
    path('images/', include('images.urls')),
    path('users/', include('accounts.urls')),
    path('albums/', include('albums.urls')),
]
