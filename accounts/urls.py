from django.urls import path
from .views import UserView

urlpatterns = [
    path('current/', UserView.as_view(), name='user'),
]