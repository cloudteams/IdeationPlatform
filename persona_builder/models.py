from httplib import BadStatusLine

import simplejson as json
import uuid
from ct_anonymizer.settings import PRODUCTION
from django.db import models
from django.db import transaction

from pb_oauth import xmlrpc_oauth

import ssl

ssl._create_default_https_context = ssl._create_unverified_context


OVERVIEW_PROPERTIES = ['gender', 'age', 'tech_level', 'platform', 'device', 'activity']


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
    overview_prop_values = models.TextField(editable=False, default='[]')
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

        # update overview values
        self.update_overview_values(self.users)

    def update_overview_values(self, users=None, commit=False):
        if not users:
            users = json.loads(self.users)

        overview_prop_values = {}
        for u in users:
            for prop in u.keys():
                # don't include properties bound by the query itself
                if prop in OVERVIEW_PROPERTIES and (prop + '=') not in self.query:
                    if prop not in overview_prop_values:
                        overview_prop_values[prop] = {}

                    # each property can have multiple values
                    vals = u[prop]
                    if type(vals) == list:
                        vals = list(set(vals))
                    else:
                        vals = [vals]

                    # vote up the correct values
                    for v in vals:
                        if v not in overview_prop_values[prop].keys():
                            overview_prop_values[prop][v] = 1
                        else:
                            overview_prop_values[prop][v] += 1

        self.overview_prop_values = overview_prop_values
        if commit:
            self.save()

    def send_campaign_personas(self, srv, exclude_self=False):
        """
        Sends the personas of this campaign to Customer Platform
        :param srv: The api connection object
        :return: the code returned by the XML-RPC API
        """
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
            try:
                result = srv.setpersona(str(self.campaign_id), personas)
                print('Personas for campaign %d sent to Team Platform' % self.campaign_id)
                return result
            except:
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
