from django.db import models

from team.models import Team


class Player(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, db_index=True)
    position = models.CharField(max_length=255)
    jersey_number = models.PositiveSmallIntegerField(null=True)
    date_of_birth = models.DateField(null=True)
    nationality = models.CharField(max_length=255)
    contract_until = models.DateField(null=True)
    market_value = models.PositiveIntegerField(null=True)
    image = models.URLField(null=True, max_length=2000)

    class Meta:
        ordering = ['jersey_number']

    def __str__(self):
        return '%s | %s | %s | %s | jersey number: %s | date of birth: %s (%s) | nationality: %s | ' \
               'contract until: %s | market value: %s €' % (
                   self.id,
                   self.team.name,
                   self.name,
                   self.position,
                   self.jersey_number,
                   self.date_of_birth,
                   self.age(),
                   self.nationality,
                   self.contract_until,
                   self.market_value,
               )

    def age(self):
        if self.date_of_birth:
            import datetime
            return int((datetime.date.today() - self.date_of_birth).days / 365.25)
        else:
            return None
