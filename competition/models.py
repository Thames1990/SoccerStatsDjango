from django.db import models


class Competition(models.Model):
    """
    The list representation of this resource is the de-facto entry point to the API and by default returns all
    available competitions for the current season.
    """
    id = models.PositiveSmallIntegerField(primary_key=True)
    is_cup = models.BooleanField()
    caption = models.CharField(max_length=255, db_index=True)
    league = models.CharField(max_length=255)
    year = models.PositiveSmallIntegerField()
    current_matchday = models.PositiveSmallIntegerField()
    number_of_matchdays = models.PositiveSmallIntegerField()
    number_of_teams = models.PositiveSmallIntegerField()
    number_of_games = models.PositiveSmallIntegerField()
    last_updated = models.DateTimeField()

    class Meta:
        ordering = ['-year', 'caption']
        get_latest_by = 'last_updated'

    def __str__(self):
        return '%s on matchday %s' % (
            self.caption,
            self.current_matchday,
        )

    def is_last_matchday(self):
        return self.current_matchday == self.number_of_matchdays

    def slug(self):
        import re

        from django.utils.text import slugify

        return slugify(re.sub('(?<=[ ]).\d+', '', self.caption))
