from django.urls import path
from .views import *

urlpatterns = [
    path('', AlbumViewSet.as_view({'get': 'list', 'post': 'create'}), name='albums'),
    path('<int:pk>/', AlbumViewSet.as_view({'get': 'retrieve', 'delete': 'destroy', 'put': 'update'}), name='album'),
    path('<int:pk>/images/add', AlbumViewSet.as_view({'patch': 'add_images'}), name='album-images'),
    path('<int:pk>/images/remove', AlbumViewSet.as_view({'patch': 'remove_images'}), name='album-images-remove'),
    path('<int:pk>/users/add', AlbumViewSet.as_view({'patch': 'add_users'}), name='album-users'),
    path('<int:pk>/users/remove', AlbumViewSet.as_view({'patch': 'remove_users'}), name='album-users-remove'),
]