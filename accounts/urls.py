from django.urls import path
from .views import UserViewSet

urlpatterns = [
    path('current/', UserViewSet.as_view({'get': 'get'}), name='current-user'),
    path('search/', UserViewSet.as_view({'get': 'search_users'}), name='search-users'),
]