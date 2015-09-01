from django.db import models
from lists import DATABASE_CONNECTION_TYPES


class ConnectionConfiguration(models.Model):
    name = models.CharField(max_length=255, unique=True)
    connection_type = models.CharField(max_length=128, choices=DATABASE_CONNECTION_TYPES)
    info = models.CharField(max_length=8128)
