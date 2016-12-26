from datetime import datetime

from django.db import models


class Competition(models.Model):
    """
    The list representation of this resource is the de-facto entry point to the API and by default returns all
    available competitions for the current season.
    """
    id = models.PositiveSmallIntegerField(primary_key=True)
    is_cup = models.BooleanField()
    caption = models.CharField(max_length=255)
    league = models.CharField(max_length=255)
    year = models.IntegerField(choices=[(y, y) for y in range(2015, datetime.now().year + 1)])
    current_matchday = models.PositiveSmallIntegerField()
    number_of_matchdays = models.PositiveSmallIntegerField()
    number_of_teams = models.PositiveSmallIntegerField()
    number_of_games = models.PositiveSmallIntegerField()
    last_updated = models.DateTimeField()

    class Meta:
        ordering = ['caption']
        get_latest_by = 'last_updated'

    def __str__(self):
        field_values = []
        for field in self._meta.get_all_field_names():
            field_values.append(getattr(self, field, ''))
        return ' '.join(field_values)

    def is_last_matchday(self):
        return self.current_matchday == self.number_of_matchdays
