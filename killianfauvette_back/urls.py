from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import Home, Root

urlpatterns = [
    path('', Root.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('token/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('jwt-test/', Home.as_view(), name='jwt-test'),
    path('images/', include('images.urls'))
]
