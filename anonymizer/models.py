import simplejson as json
import uuid
from django.db import models
from anonymizer.datasource.connections import ConnectionManager
from anonymizer.datasource.managers.users import UserManager
from lists import DATABASE_CONNECTION_TYPES


class ConnectionConfiguration(models.Model):
    name = models.CharField(max_length=255, unique=True)
    connection_type = models.CharField(max_length=128, choices=DATABASE_CONNECTION_TYPES)
    info = models.CharField(max_length=8128)

    users_table = models.CharField(max_length=256, default='')
    user_pk = models.CharField(max_length=256, default='')

    properties = models.TextField(default='')
    foreign_keys = models.TextField(default='', editable=False)

    # only one configuration should be active at each time
    is_active = models.BooleanField(default=False, editable=False)

    def update_info_url(self):
        base_url = '/anonymizer/connection/update-info'

        if self.connection_type == 'django.db.backends.sqlite3':
            return '{0}/{1}/sqlite3/'.format(base_url, self.pk)
        elif self.connection_type == 'django.db.backends.mysql':
            return '{0}/{1}/mysql/'.format(base_url, self.pk)
        elif self.connection_type == 'django.db.backends.psycopg2':
            return '{0}/{1}/postgres/'.format(base_url, self.pk)

    def get_default_properties(self, columns):
        properties = []

        for column in columns[1:]:
            # auto-create property name
            from_table = column[2].split('.')[0]
            if from_table.lower() == self.users_table.lower():
                name = column[0]
            else:
                name = from_table + '_' + column[0]

            # set initial form data
            properties.append({
                'name': name,
                'type': column[1],
                'source': column[2],
            })

        return json.dumps(properties)

    def info_to_json(self):
        """
        :return: Connection info to json (without brackets)
        """
        obj = json.loads('[{%s}]' % self.info)
        obj[0]['id'] = self.name
        obj[0]['engine'] = self.connection_type

        return obj

    def to_json(self):
        """
        :return: The whole configuration as a json string
        """
        obj = {
            "sites": [{
                "name": self.name,

                "connections": self.info_to_json(),

                "user_pk": self.user_pk,
                "properties": json.loads(self.properties),
                "foreign_keys": json.loads(self.foreign_keys),
            }]
        }

        return json.dumps(obj, indent=4)

    def get_connection(self):
        manager = ConnectionManager(self.info_to_json())
        return manager.get(self.name)

    def get_user_manager(self, token=None):
        if not token:
            token = uuid.uuid4()

        return UserManager(from_str=self.to_json(), token=token)

    def save(self, *args, **kwargs):
        if ConnectionConfiguration.objects.all().count() == 0:
            self.is_active = True

        super(ConnectionConfiguration, self).save(*args, **kwargs)