from django.db import models
from django.contrib.auth.models import User
from images.models import Image

class AlbumImage(models.Model):
    image = models.ForeignKey('images.Image', on_delete=models.CASCADE)
    album = models.ForeignKey('Album', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.album.title} - {self.image.url}"


class AlbumUser(models.Model):
    album = models.ForeignKey('Album', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.album.title} - {self.user.username}"


class Album(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(default='', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    password_accessible = models.BooleanField(default=False)
    password = models.CharField(default='', null=False, blank=False, max_length=1000)
    belongs_to = models.ManyToManyField(User, through='AlbumUser', related_name='albums')
    images = models.ManyToManyField(Image, through='AlbumImage', related_name='albums')

    def add_images(self, images):
        for image in images:
            AlbumImage.objects.create(image=image, album=self)

    def remove_images(self, images):
        for image in images:
            self.belongs_to.remove(image)

    def add_users(self, users):
        for user in users:
            AlbumUser.objects.create(user=user, album=self)

    def remove_users(self, users):
        for user in users:
            self.belongs_to.remove(user)

    def get_users(self):
        return self.belongs_to.all()

    def get_images(self):
        return self.images.all()



    def __str__(self):
        return self.title
