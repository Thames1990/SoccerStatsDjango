from djmoney.models.fields import MoneyField
from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    short_name = models.CharField(max_length=255)
    squad_market_value = MoneyField(max_digits=10, decimal_places=0, default_currency='EUR')
    crest_url = models.URLField(null=True)
