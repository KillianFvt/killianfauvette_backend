from django.contrib import admin
from .models import Album, AlbumImage, AlbumUser

admin.site.register(Album)
admin.site.register(AlbumImage)
admin.site.register(AlbumUser)
