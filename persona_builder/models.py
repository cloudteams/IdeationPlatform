import simplejson as json
import uuid
from django.contrib.auth.models import User
from django.db import models


class Persona(models.Model):
    uuid = models.UUIDField(unique=True, primary_key=False, default=uuid.uuid4, editable=False)
    owner = models.CharField(max_length=255, null=True, blank=True, default='')
    name = models.CharField(max_length=256, null=False, blank=False, unique=True)
    description = models.CharField(max_length=4096, null=False, blank=False)
    avatar = models.ImageField(upload_to='persona-avatars', null=True, blank=True)
    query = models.TextField(editable=False)
    users = models.TextField(editable=False, default='[]')
    is_ready = models.BooleanField(default=False, editable=False)
    is_public = models.BooleanField(default=False)

    def get_avatar_url(self):
        return '/media/%s' % self.avatar

    def get_absolute_url(self):
        return '/persona-builder/personas/%s/' % self.pk

    def get_edit_properties_url(self):
        return self.get_absolute_url() + 'edit-properties/'

    def update_users(self, user_manager):
        old_users = json.loads(self.users)
        new_users = user_manager.filter(self.query)

        # combine the two sets
        users = user_manager.combine(old_users, new_users)
        self.users = json.dumps(users)
