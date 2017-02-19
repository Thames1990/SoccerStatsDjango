from django.db import models
from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFill

from competition.models import Competition


class Team(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
    competition = models.ManyToManyField(Competition)
    name = models.CharField(max_length=255, db_index=True)
    code = models.CharField(null=True, max_length=255)
    short_name = models.CharField(null=True, max_length=255)
    squad_market_value = models.PositiveIntegerField(null=True)
    logo = models.ImageField(upload_to='logos', null=True)
    logo_thumbnail = ImageSpecField(
        source='avatar',
        processors=[ResizeToFill(100, 50)],
        format='JPEG',
        options={'quality': 60}
    )

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

    def __str__(self):
        return self.name
