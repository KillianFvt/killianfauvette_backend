from django.contrib.auth.models import User
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from cookie_token.auth_class import CookieJWTAuthentication
from .models import Image
from .serializers import ImageSerializer


class ImageViewSet(viewsets.ModelViewSet):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve an image
        """
        # TODO add logic to check if the user has access to the image
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """
        Creates an image
        get the name, url, has_watermark and belongs_to from the request data
        if belongs_to is not provided, it defaults to the admin user
        if has_watermark is not provided, it defaults to False
        """


        belongs_to = request.data.get('belongs_to')

        if not belongs_to:
            belongs_to = []

        users = []

        for user_id in belongs_to:
            try:
                user = User.objects.get(id=user_id)
                users.append(user)
            except User.DoesNotExist:
                return Response({'error': f'User {user_id} not found'}, status=status.HTTP_404_NOT_FOUND)

        images = request.data.get('images')
        if not images:
            return Response({'error': 'images is required'}, status=status.HTTP_400_BAD_REQUEST)

        created_images = []

        for image in images:

            name = image.get('name')
            url = image.get('url')
            has_watermark = image.get('has_watermark')

            if not name or not url:
                return Response({'error': 'name and url are required for every image'}, status=status.HTTP_400_BAD_REQUEST)
            if not has_watermark:
                has_watermark = False

            try:
                new_image = Image.objects.create(name=name, url=url, has_watermark=has_watermark)
                new_image.add_users(users)
                new_image.save()
                created_images.append(new_image)
            except Exception as e:
                for created_image in created_images:
                    created_image.delete()
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'details': 'image created',
            'image_ids': [image.id for image in created_images],
        }, status=status.HTTP_201_CREATED)


    def list(self, request, *args, **kwargs):
        """
        List all images for a user
        if the user is not staff, only images that belong to the user are returned
        """
        if not request.user.is_staff:
            queryset = Image.objects.filter(belongs_to=request.user)
            serializer = ImageSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return super().list(request, *args, **kwargs)

    @action(detail=True, methods=['patch'])
    def add_users(self, request, pk=None):
        """
        Add users to an image
        get the user_ids from the request data
        """

        image = self.get_object()
        user_ids = request.data.get('user_ids')
        if not user_ids:
            user_ids = []

        for user_id in user_ids:
            try:
                user = User.objects.get(id=user_id)
                image.belongs_to.add(user)
            except User.DoesNotExist:
                return Response({'error': f'User {user_id} not found'}, status=status.HTTP_404_NOT_FOUND)

        image.save()
        return Response({'details': f'users {user_ids} added'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'])
    def remove_users(self, request, pk=None):
        """
        Remove users from an image
        get the user_ids from the request data
        """
        image = self.get_object()
        user_ids = request.data.get('user_ids')
        if not user_ids:
            user_ids = []
        for user_id in user_ids:
            try:
                user = User.objects.get(id=user_id)
                image.belongs_to.remove(user)
            except User.DoesNotExist:
                return Response({'error': f'User {user_id} not found'}, status=status.HTTP_404_NOT_FOUND)

        image.save()
        return Response({'details': f'users {user_ids} removed'}, status=status.HTTP_200_OK)
