from django.db import models

from competition.models import Competition


class Team(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
    competition = models.ManyToManyField(Competition)
    name = models.CharField(max_length=255, db_index=True)
    code = models.CharField(null=True, max_length=255)
    short_name = models.CharField(null=True, max_length=255)
    squad_market_value = models.PositiveIntegerField(null=True)
    crest_url = models.URLField(null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_squad_market_value(self):
        """
        Calculates the squad market value
        :return: Squad market value
        """
        if self.squad_market_value:
            return self.squad_market_value
        else:
            squad_market_value = 0
            for player in self.player_set.all():
                if player.market_value:
                    squad_market_value += player.market_value
            return squad_market_value

    def slug(self):
        from django.utils.text import slugify

        return slugify(self.name)
