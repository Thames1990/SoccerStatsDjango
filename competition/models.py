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
    year = models.PositiveSmallIntegerField()
    current_matchday = models.PositiveSmallIntegerField()
    number_of_matchdays = models.PositiveSmallIntegerField()
    number_of_teams = models.PositiveSmallIntegerField()
    number_of_games = models.PositiveSmallIntegerField()
    last_updated = models.DateTimeField()

    class Meta:
        ordering = ['caption']
        get_latest_by = 'last_updated'

    def __str__(self):
        return 'id: %s, cup: %s | %s | %s | %s, matchday %s of %s | %s teams | %s games | %s' % (
            self.id,
            self.is_cup,
            self.caption,
            self.league,
            self.year,
            self.current_matchday,
            self.number_of_matchdays,
            self.number_of_teams,
            self.number_of_games,
            self.last_updated,
        )

    def is_last_matchday(self):
        return self.current_matchday == self.number_of_matchdays
