import simplejson as json
import uuid
from ct_anonymizer.settings import PRODUCTION
from django.db import models
from django.db import transaction
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver


class Persona(models.Model):
    uuid = models.UUIDField(unique=True, primary_key=False, default=uuid.uuid4, editable=False)
    owner = models.CharField(max_length=255, null=True, blank=True, default='')
    project_id = models.IntegerField(blank=True, null=True, default=None)
    campaign_id = models.IntegerField(blank=True, null=True, default=None)
    name = models.CharField(max_length=256, null=False, blank=False)
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

    def get_edit_info_url(self):
        return self.get_absolute_url() + 'edit-info/'

    def update_users(self, user_manager):
        old_users = json.loads(self.users)
        new_users = user_manager.filter(self.query, true_id=True)

        # combine the two sets
        users = user_manager.combine(old_users, new_users)
        self.users = json.dumps(users)

        # update persona user entries
        with transaction.atomic():
            PersonaUsers.objects.filter(persona=self).delete()
            for user in users:
                PersonaUsers.objects.create(persona=self, user_id=user['__id__'])


@receiver(post_save, sender=Persona)
def on_create_persona(sender, instance, created, **kwargs):
    # Only on production
    if not PRODUCTION:
        return

    # Only when instance was created
    if created:
        pass


@receiver(pre_delete, sender=Persona)
def on_delete_persona(sender, instance, using, **kwargs):
    # Only on production
    if not PRODUCTION:
        return
    
    pass


class PersonaUsers(models.Model):
    """
    Users represented by each persona
    """
    persona = models.ForeignKey(Persona)
    user_id = models.TextField()
