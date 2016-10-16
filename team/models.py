from djmoney.models.fields import MoneyField
from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    short_name = models.CharField(max_length=255)
    squad_market_value = models.PositiveIntegerField()
    crest_url = models.URLField(null=True)
