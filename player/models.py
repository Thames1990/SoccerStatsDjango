from django.db import models

from team.models import Team


class Player(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    jersey_number = models.PositiveSmallIntegerField(null=True)
    date_of_birth = models.DateField(null=True)
    nationality = models.CharField(max_length=255)
    contract_until = models.DateField(null=True)
    market_value = models.PositiveIntegerField(null=True)
    image = models.URLField(null=True)

    class Meta:
        ordering = ['jersey_number']

    def age(self):
        import datetime
        return int((datetime.date.today() - self.date_of_birth).days / 365.25)
