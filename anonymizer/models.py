import json
from django.db import models
from lists import DATABASE_CONNECTION_TYPES


class ConnectionConfiguration(models.Model):
    name = models.CharField(max_length=255, unique=True)
    connection_type = models.CharField(max_length=128, choices=DATABASE_CONNECTION_TYPES)
    info = models.CharField(max_length=8128)

    users_table = models.CharField(max_length=256, default='')
    total = models.CharField(max_length=16384, default='')

    def update_info_url(self):
        base_url = '/anonymizer/connection/update-info'

        if self.connection_type == 'django.db.backends.sqlite3':
            return '{0}/{1}/sqlite3/'.format(base_url, self.pk)
        elif self.connection_type == 'django.db.backends.mysql':
            return '{0}/{1}/mysql/'.format(base_url, self.pk)

    def info_to_json(self):
        """
        :return: Connection info to json (without brackets)
        """
        obj = json.loads('[{%s}]' % self.info)
        obj[0]['id'] = self.name
        obj[0]['engine'] = self.connection_type

        return obj

    def create_json(self, user_pk_source, properties):
        """
        :return: The whole configuration as a json string
        """
        obj = {
            "sites": [{
                "name": self.name,

                "connections": self.info_to_json(),

                "user_pk": user_pk_source,
                "properties": properties
            }]
        }

        return json.dumps(obj, indent=4)
