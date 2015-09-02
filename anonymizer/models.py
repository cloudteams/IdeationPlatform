import json
from django.db import models
from lists import DATABASE_CONNECTION_TYPES


class ConnectionConfiguration(models.Model):
    name = models.CharField(max_length=255, unique=True)
    connection_type = models.CharField(max_length=128, choices=DATABASE_CONNECTION_TYPES)
    info = models.CharField(max_length=8128)

    users_table = models.CharField(max_length=256, default='')

    def update_info_url(self):
        base_url = '/anonymizer/connection/update-info'

        if self.connection_type == 'django.db.backends.sqlite3':
            return '{0}/{1}/sqlite3/'.format(base_url, self.pk)
        elif self.connection_type == 'django.db.backends.mysql':
            return '{0}/{1}/mysql/'.format(base_url, self.pk)

    def info_to_json(self):
        obj = json.loads('[{%s}]' % self.info)
        obj[0]['id'] = self.name
        obj[0]['engine'] = self.connection_type

        return obj
