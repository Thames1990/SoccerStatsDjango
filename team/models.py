from django.db import models

from competition.models import Competition


class Team(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
    competition = models.ManyToManyField(Competition)
    name = models.CharField(max_length=255)
    code = models.CharField(null=True, max_length=255)
    short_name = models.CharField(null=True, max_length=255)
    squad_market_value = models.PositiveIntegerField(null=True)
    crest_url = models.URLField(null=True)
