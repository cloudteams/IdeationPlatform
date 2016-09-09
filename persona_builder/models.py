from httplib import BadStatusLine

import datetime

import cjson
import simplejson as json
import uuid

import sys

import thread

from ct_anonymizer.settings import PRODUCTION, MIN_USERS_IN_PERSONA
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
    overview_prop_values = models.TextField(editable=False, default='[]')
    is_ready = models.BooleanField(default=False, editable=False)
    is_public = models.BooleanField(default=False)
    based_on = models.ForeignKey('self', blank=True, null=True, default=None)
    is_processing = models.BooleanField(default=False)

    def get_avatar_url(self):
        return '/media/%s' % self.avatar

    def get_absolute_url(self):
        return '/persona-builder/personas/%s/' % self.pk

    def get_edit_properties_url(self):
        return self.get_absolute_url() + 'edit-properties/'

    def get_edit_info_url(self):
        return self.get_absolute_url() + 'edit-info/'

    def _do_update_users(self, new_users):
        with transaction.atomic():
            for u in new_users:
                PersonaUsers.objects.create(persona=self, user_id=u['__id__'], info=cjson.encode(u))

        print 'Persona %d updated successfully.' % self.pk

    def update_users(self, user_manager, async=False):
        new_users = user_manager.filter(self.query, true_id=True)

        # check if minimum users requirement is validated
        if len(new_users) < MIN_USERS_IN_PERSONA:
            return False

        # update overview values
        self.update_overview_values(new_users)

        # remove previous users
        PersonaUsers.objects.filter(persona=self).delete()

        # save persona users
        if async:
            # Persona.objects.filter(pk=self.pk).update(is_processing=True)
            thread.start_new_thread(self._do_update_users, (new_users, ))
        else:
            self._do_update_users(new_users)

        return True

    def get_overview_values(self):
        return json.loads(self.overview_prop_values)

    def update_overview_values(self, users=None, commit=False):
        if users:
            qs = users
        else:
            qs = PersonaUsers.objects.filter(persona=self)

        overview_prop_values = {}
        for u in qs:
            # get user info
            if type(u) == PersonaUsers:
                u = json.loads(u.info)

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

        self.overview_prop_values = json.dumps(overview_prop_values)
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
    info = models.TextField()
