from django.db import models


class Player(models.Model):
    name = models.CharField(max_length=255)
    KEEPER = 1
    RIGHT_BACK = 2
    CENTRE_BACK = 4
    LEFT_BACK = 3
    DEFENSIVE_MIDFIELD = 6
    CENTRAL_MIDFIELD = 8
    ATTACKING_MIDFIELD = 10
    RIGHT_WING = 7
    CENTRE_FORWARD = 9
    LEFT_WING = 11
    POSITION = (
        (KEEPER, 'Keeper'),
        (RIGHT_BACK, 'Right-Back'),
        (CENTRE_BACK, 'Centre Back'),
        (LEFT_BACK, 'Left-Back'),
        (DEFENSIVE_MIDFIELD, 'Defensive Midfield'),
        (CENTRAL_MIDFIELD, 'Central Midfield'),
        (ATTACKING_MIDFIELD, 'Attacking Midfield'),
        (RIGHT_WING, 'Right Wing'),
        (CENTRE_FORWARD, 'Centre Forward'),
        (LEFT_WING, 'Left Wing'),
    )
    position = models.CharField(max_length=255, choices=POSITION)
    jersey_number = models.PositiveSmallIntegerField()
    date_of_birth = models.DateField()
    nationality = models.CharField(max_length=255)
    contract_until = models.DateField(null=True)
    market_value = models.PositiveIntegerField(null=True)
    image = models.URLField(null=True)

    class Meta:
        ordering = ['position']

    def age(self):
        import datetime
        return int((datetime.date.today() - self.date_of_birth).days / 365.25)
