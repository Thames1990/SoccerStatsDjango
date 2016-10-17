from django.db import models


class Team(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    short_name = models.CharField(max_length=255)
    squad_market_value = models.PositiveIntegerField(null=True)
    crest_url = models.URLField(null=True)
