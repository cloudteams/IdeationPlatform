from django.contrib.auth.models import User
from django.db import models


class Persona(models.Model):
    owner = models.ForeignKey(User, blank=True, null=True)
    name = models.CharField(max_length=256, null=False, blank=False, unique=True)
    description = models.CharField(max_length=4096, null=False, blank=False)
    avatar = models.ImageField(upload_to='persona-avatars')
    query = models.CharField(max_length=4096, editable=False)
    users = models.CharField(max_length=16256, editable=False)
    is_ready = models.BooleanField(default=False, editable=False)
    is_public = models.BooleanField(default=False)

    def get_avatar_url(self):
        return '/media/%s' % self.avatar

    def get_absolute_url(self):
        return '/persona-builder/personas/%d/' % self.pk

    def get_edit_properties_url(self):
        return self.get_absolute_url() + 'edit-properties/'
