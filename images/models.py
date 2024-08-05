from django.contrib.auth.models import User
from django.db import models


class UserImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ForeignKey('Image', on_delete=models.CASCADE)


class Image(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField(null=False, blank=False, unique=True)
    uploaded = models.DateTimeField(auto_now_add=True)
    has_watermark = models.BooleanField(default=False)
    belongs_to = models.ManyToManyField(User, through='UserImage', related_name='images', blank=True)

    class Meta:
        ordering = ['uploaded']
        verbose_name = 'Image'
        verbose_name_plural = 'Images'

    def upload(self):
        # TODO add CDN upload logic here
        print(f"Uploading image {self.url} to CDN")
        super().save()

    def delete(self, *args, **kwargs):
        # TODO add CDN delete logic here
        print(f"Deleting image {self.url} from CDN")
        super().delete(*args, **kwargs)

    def get_users(self):
        return self.belongs_to.all()

    def __str__(self):
        return self.url

    def __repr__(self):
        return self.url

    def __eq__(self, other):
        if isinstance(other, Image):
            return self.url == other.url
        return False

    def __ne__(self, other):
        return not self.__eq__(other)
