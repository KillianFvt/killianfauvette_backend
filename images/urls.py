from django.urls import path
from .views import ImageViewSet

urlpatterns = [
    path('', ImageViewSet.as_view({'get': 'list', 'post': 'create'}), name='images'),
    path('<int:pk>/', ImageViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy',
        'patch': 'partial_update'
    }), name='image'),
    path('<int:pk>/add_users/', ImageViewSet.as_view({'patch': 'add_users'}), name='image-add-user'),
    path('<int:pk>/remove_users/', ImageViewSet.as_view({'patch': 'remove_users'}), name='image-remove-user'),
]
