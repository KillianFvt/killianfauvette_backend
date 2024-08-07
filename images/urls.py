from django.urls import path
from .views import ImageViewSet

urlpatterns = [
    path('all/', ImageViewSet.as_view({'get': 'list'}), name='images-all'),
    path('create/', ImageViewSet.as_view({'post': 'create'}), name='images-create'),
    path('update/<int:pk>/', ImageViewSet.as_view({'put': 'update'}), name='images-update'),
    path('delete/<int:pk>/', ImageViewSet.as_view({'delete': 'destroy'}), name='images-delete'),
    path('<int:pk>/', ImageViewSet.as_view({'get': 'retrieve'}), name='images-retrieve'),
]
