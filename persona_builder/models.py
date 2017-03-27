from httplib import BadStatusLine

import datetime

import cjson
import simplejson as json
import uuid

import sys

import thread

from ct_anonymizer.settings import PRODUCTION, MIN_USERS_IN_PERSONA, MEDIA_URL
from django.db import models
from django.db import transaction

from pb_oauth import xmlrpc_oauth

import ssl

ssl._create_default_https_context = ssl._create_unverified_context


OVERVIEW_PROPERTIES = ['gender', 'age', 'tech_level', 'platform', 'device', 'education', 'employment']


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

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        _public = ''
        if self.is_public:
            _public = ' (public persona)'

        _cnt = ' - %d users matched' % PersonaUsers.objects.filter(persona_id=self.pk).count()

        return '%s%s%s' % (self.name, _public, _cnt)

    def get_avatar_url(self):
        if PRODUCTION:
            base_url = 'https://customers.cloudteams.eu/team-ideation-tools'
        else:
            base_url = 'http://127.0.0.1:8000'

        if not self.avatar:
            return '%s/static/persona_builder/img/default-persona.svg' % base_url

        return '%s/media/%s' % (base_url, self.avatar)

    def get_absolute_url(self, full=False):
        if not full:
            return '/team-ideation-tools/personas/%s/' % self.pk
        else:
            return '/team-ideation-tools/personas/?persona=%s&action=details' % self.pk

    def get_edit_properties_url(self, full=False):
        if not full:
            return '/team-ideation-tools/personas/%s/edit-properties/' % self.pk
        else:
            return '/team-ideation-tools/personas/?persona=%s&action=edit-properties' % self.pk

    def get_edit_info_url(self, full=False):
        if not full:
            return '/team-ideation-tools/personas/%s/edit-info/' % self.pk
        else:
            return '/team-ideation-tools/personas/?persona=%s&action=edit-info' % self.pk

    @property
    def properties(self):
        query = self.query
        result = []

        # turn [(activity="Running")] to (activity="Running")
        if query.startswith('['):
            query = query[1:-1]

        # turn activity="Running" to (activity="Running")
        if '(' not in query:
            query = '(' + query + ')'

        # split parts based on parentheses
        # remember - no support for multiple levels & complex logic
        parts = query.split('(')
        for i, f in enumerate(parts):
            # ignore first part - empty
            if i == 0:
                continue

            # detect different parts of the expression
            # e.g activity!="Running" must be split into activity / != / Running
            exp = ["", "", ""]
            ptr = 0
            special = False
            symbols = ['=', '<', '>', '!']
            for c in f:
                if (c in symbols) != special:
                    special = not special
                    ptr += 1

                # end of property
                if c == ')':
                    break

                if c != '"':
                    exp[ptr] += c

            # find the values -- could be more than one
            vals = exp[2].split('||')

            # add the key-value object
            if exp[0]:
                result.append({'field': exp[0], 'values': vals})

        return result

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

    def get_overview_values(self, n=6, cutoff=0.05):
        """
        :param n: Number of most popular options to fetch. Remaining options will be grouped in an 'Other' options
        :param cutoff: A percentage under which an option will also be assigned to 'Other'
        :return: A dictionary of the following form: {'Device': [('Mobile', 12), ('Desktop', 10), ('Other', 2)], ...}
        """
        result = {}
        data = json.loads(self.overview_prop_values)

        # sort
        for p in data:
            # get total & avoid empty list manipulation
            total = sum([data[p][v] for v in data[p]])

            if total == 0:
                return []

            # sort options by popularity
            p_list = sorted([(v, data[p][v]) for v in data[p]], key=lambda x: x[1], reverse=True)

            # remove options under cutoff
            other_sum = 0
            head = []
            for x in p_list[:n]:
                if float(x[1])/total >= cutoff:
                    head.append(x)
                else:
                    other_sum += x[1]

            # only first n options
            if len(p_list) > n:
                p_list = head + [('Other', other_sum + sum([x[1] for x in p_list[n+1:]])), ]

            # add to result
            result[p] = p_list

        return result

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
            'descr': persona.description,
            'num_matches': str(PersonaUsers.objects.filter(persona_id=persona.pk).count()),
            'img': persona.get_avatar_url(),
            'date_created': persona.created.strftime('%d/%m/%y %H:%M'),
            'date': persona.updated.strftime('%d/%m/%y %H:%M'),
        } for persona in qs]

        print('ps=%s' % str(personas))
        # call method & return code
        if PRODUCTION:
            try:
                result = srv.setpersona(str(self.campaign_id), personas)
                print('Personas for campaign %d sent to Team Platform' % self.campaign_id)
                return result
            except:
                print('Error on Team Platform notification')
                return -1

    # get persona size
    @property
    def size(self):
        return PersonaUsers.objects.filter(persona_id=self.pk).count()

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
