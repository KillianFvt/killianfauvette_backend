from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from cookie_token.auth_class import CookieJWTAuthentication
from images.models import Image
from images.serializers import ImageSerializer
from .models import Album
from .serializers import AlbumSerializer


def get_album(album_id: int) -> Album | Response:
    try:
        album = Album.objects.get(id=album_id)
        return album
    except Album.DoesNotExist:
        return Response({'error': f'Album {album_id} not found'}, status=status.HTTP_404_NOT_FOUND)


def get_album_images(request) -> list[Image] | Response:
    image_ids = request.data.get('image_ids')

    if not image_ids:
        return Response({'error': 'image_ids is required'}, status=status.HTTP_400_BAD_REQUEST)

    images = []

    for image_id in image_ids:
        try:
            image = Image.objects.get(id=image_id)
            images.append(image)
        except Image.DoesNotExist:
            return Response({'error': f'Image {image_id} not found'}, status=status.HTTP_404_NOT_FOUND)

    return images


def get_users_or_404(user_ids: list[int]) -> list[User] | Response:
    users = []
    for user_id in user_ids:
        try:
            user = User.objects.get(id=user_id)
            users.append(user)
        except User.DoesNotExist:
            return Response({'error': f'User {user_id} not found'}, status=status.HTTP_404_NOT_FOUND)

    return users

class AlbumViewSet(viewsets.ModelViewSet):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Album.objects.all()
    serializer_class = AlbumSerializer

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve an album
        """
        album = self.get_object()

        if not request.user.is_staff:
            if request.user not in album.get_users():
                return Response(
                    {'error': 'You do not have permission to view this album'},
                    status=status.HTTP_403_FORBIDDEN
                )

        if isinstance(album, Response):
            return album

        images = album.get_images()

        album_serializer = AlbumSerializer(album)
        album_data = album_serializer.data

        image_serializer = ImageSerializer(images, many=True)

        album_data['images'] = [image for image in image_serializer.data]

        return Response(album_data)

    def create(self, request, *args, **kwargs):
        """
        Creates an album
        get the title, description, images and belongs_to from the request data
        if belongs_to is not provided, it defaults to the admin user

        usage : first upload images and then create album with image_ids
        """
        title = request.data.get('title')
        description = request.data.get('description')
        belongs_to = request.data.get('belongs_to')
        password_accessible = request.data.get('password_accessible')
        password = request.data.get('password')
        image_ids = request.data.get('image_ids')

        if not title:
            return Response({'error': 'title is required'}, status=status.HTTP_400_BAD_REQUEST)
        if not description:
            description = ''
        if password_accessible is None:
            return Response({'error': 'password_accessible is required'}, status=status.HTTP_400_BAD_REQUEST)
        if password_accessible and not password:
            return Response({'error': 'password is required if password_accessible=true'},
                            status=status.HTTP_400_BAD_REQUEST)
        if not belongs_to:
            belongs_to = []
        if not image_ids:
            image_ids = []

        users = []

        for user_id in belongs_to:
            try:
                user = User.objects.get(id=user_id)
                users.append(user)
            except User.DoesNotExist:
                return Response({'error': f'User {user_id} not found'}, status=status.HTTP_404_NOT_FOUND)

        images = []

        for image_id in image_ids:
            try:
                image = Image.objects.get(id=image_id)
                images.append(image)
            except Image.DoesNotExist:
                return Response({'error': f'Image {image_id} not found'}, status=status.HTTP_404_NOT_FOUND)

        album = Album.objects.create(
            title=title,
            description=description,
            password_accessible=password_accessible,
        )
        album.add_users(users)
        album.save()

        album.add_images(images)

        return Response({
            'details': 'album created',
            'album_id': album.id,
        }, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """
        Update an album

        usage :
            - for image addition : first upload images and then add images to album with image_ids
            - for image removal : deleting images will automatically remove images from album
            - for user addition : add users to album with user_ids
            - for user removal : remove users from album with user_ids
        """
        belongs_to = request.data.get('belongs_to')

        if belongs_to is None:
            return Response({'error': 'belongs_to is required'}, status=status.HTTP_400_BAD_REQUEST)

        album = self.get_object()
        previous_users_ids = [user.id for user in album.get_users()]
        users_to_add = []
        users_to_remove = []

        for user_id in belongs_to:
            if user_id not in previous_users_ids:
                users_to_add.append(user_id)

        for user_id in previous_users_ids:
            if user_id not in belongs_to:
                users_to_remove.append(user_id)

        users_to_add = get_users_or_404(users_to_add)
        users_to_remove = get_users_or_404(users_to_remove)

        album.add_users(users_to_add)
        album.remove_users(users_to_remove)

        return super().update(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        """
        List all albums
        """
        albums = Album.objects.filter(belongs_to=request.user)
        serializer = AlbumSerializer(albums, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['patch'])
    def add_images(self, request, *args, **kwargs):
        """
        Add images to an album
        """

        album_id = kwargs.get('pk')
        album = get_album(album_id)
        if isinstance(album, Response):
            return album

        images = get_album_images(request)
        if isinstance(images, Response):
            return images

        album.add_images(images)

        return Response({'details': 'images added to album'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['patch'])
    def remove_images(self, request, *args, **kwargs):
        """
        Remove images from an album
        """
        album_id = kwargs.get('pk')
        album = get_album(album_id)
        if isinstance(album, Response):
            return album

        images = get_album_images(request)
        if isinstance(images, Response):
            return images

        album.remove_images(images)

        return Response({'details': 'images removed from album'}, status=status.HTTP_200_OK)


    @action(detail=False, methods=['patch'])
    def add_users(self, request, *args, **kwargs):
        """
        Add users to an album
        """

        album_id = kwargs.get('pk')
        album = get_album(album_id)
        if isinstance(album, Response):
            return album

        users = get_users_or_404(request.data.get('user_ids'))
        if isinstance(users, Response):
            return users

        album.add_users(users)

        for image in album.get_images():
            image.add_users(users)

        return Response({'details': 'users added to album'}, status=status.HTTP_200_OK)


    @action(detail=False, methods=['patch'])
    def remove_users(self, request, *args, **kwargs):
        """
        Remove users from an album
        """
        album_id = kwargs.get('pk')
        album = get_album(album_id)
        if isinstance(album, Response):
            return album

        users = get_users_or_404(request.data.get('user_ids'))
        if isinstance(users, Response):
            return users

        album.remove_users(users)

        for image in album.get_images():
            image.remove_users(users)

        return Response({'details': 'users removed from album'}, status=status.HTTP_200_OK)