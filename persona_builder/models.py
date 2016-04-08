from httplib import BadStatusLine

import simplejson as json
import uuid
from ct_anonymizer.settings import PRODUCTION, SERVER_URL, USER_PASSWD
from django.db import models
from django.db import transaction
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from pb_oauth.xmlrpc_oauth import get_srv_instance
from pb_oauth.xmlrpc_srv import XMLRPC_Server

import ssl

ssl._create_default_https_context = ssl._create_unverified_context


class Persona(models.Model):
    uuid = models.UUIDField(unique=True, primary_key=False, default=uuid.uuid4, editable=False)
    owner = models.CharField(max_length=255, null=True, blank=True, default='')
    project_id = models.IntegerField(blank=True, null=True, default=None)
    campaign_id = models.IntegerField(blank=True, null=True, default=None)
    name = models.CharField(max_length=256, null=False, blank=False)
    description = models.TextField(null=True, blank=True, default='')
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

    def send_campaign_personas(self, request, exclude_self=False):
        """
        Sends the personas of this campaign to Customer Platform
        :param request: The request object
        :return: the code returned by the XML-RPC API
        """
        server = request.session['server']
        oauth_credentials = request.session['bswc_token']

        # get list of personas
        qs = Persona.objects.filter(campaign_id=self.campaign_id).exclude(owner='SYSTEM')
        if exclude_self:
            qs = qs.exclude(id=self.id)

        # create the parameter for the api call
        personas = [{
            'id': str(persona.id),
            'name': persona.name,
            'descr': persona.description
        } for persona in qs]

        # call method & return code
        if PRODUCTION:
            srv = get_srv_instance(request.user.username)
            if not srv:
                print('No credentials object')
                return -1
            try:
                result = srv.setpersona(str(self.campaign_id), personas)
                print('Personas for campaign %d sent to Team Platform' % self.campaign_id)
                return result
            except BadStatusLine:
                print('Error on Team Platform notification')
                return -1

    # weird UUID bug fix
    def save(self, *args, **kwargs):
        if type(self.uuid) in [str, unicode]:
            self.uuid = self.uuid.strip()

        super(Persona, self).save(*args, **kwargs)


class PersonaUsers(models.Model):
    """
    Users represented by each persona
    """
    persona = models.ForeignKey(Persona, db_index=True)
    user_id = models.IntegerField(db_index=True)
