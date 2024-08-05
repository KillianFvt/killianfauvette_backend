from django.shortcuts import render
from rest_framework import viewsets
from .models import Image
from .serializers import ImageSerializer


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        if user_id:
            return Image.objects.filter(user=user_id)
        return Image.objects.all()

