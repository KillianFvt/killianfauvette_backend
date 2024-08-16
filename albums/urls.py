from django.urls import path
from .views import *

urlpatterns = [
    path('', AlbumViewSet.as_view({'get': 'list', 'post': 'create'}), name='albums'),
    path('<int:pk>/', AlbumViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'}), name='album'),
    path('<int:pk>/images/add', AlbumViewSet.as_view({'patch': 'add_images'}), name='album-images'),
    path('<int:pk>/images/remove', AlbumViewSet.as_view({'patch': 'remove_images'}), name='album-images-remove'),
]