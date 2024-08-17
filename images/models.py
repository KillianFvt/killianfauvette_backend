from django.contrib.auth.models import User
from django.db import models, IntegrityError


class UserImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ForeignKey('Image', on_delete=models.CASCADE)

    class Meta:
        unique_together = ['user', 'image']


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

    def get_users(self) -> list[User]:
        return self.belongs_to.all()

    def add_users(self, users) -> None:
        for user in users:
            try:
                UserImage.objects.create(user=user, image=self)
            except IntegrityError:
                continue

    def remove_users(self, users):
        for user in users:
            try:
                UserImage.objects.get(user=user, image=self).delete()
            except UserImage.DoesNotExist:
                continue

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
