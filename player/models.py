from django.db import models

from team.models import Team


class Player(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    POSITION = (
        ('Keeper', 'Torwart'),
        ('Right-Back', 'Rechter Außenverteidiger'),
        ('Centre Back', 'Innenverteidiger'),
        ('Left-Back', 'Linker Außenverteidiger'),
        ('Defensive Midfield', 'Defensives Mittelfeld'),
        ('Left Midfield', 'Linkes Mittelfeld'),
        ('Central Midfield', 'Zentrales Mittelfeld'),
        ('Midfield', 'Mittelfeld'),
        ('Mittelfeld', 'Mittelfeld'),
        ('Right Midfield', 'Rechtes Mittelfeld'),
        ('Attacking Midfield', 'Offensives Mittelfeld'),
        ('Right Wing', 'Rechter Flügel'),
        ('Secondary Striker', 'Hängende Spitze'),
        ('Centre Forward', 'Stürmer'),
        ('Left Wing', 'Linker Flügel'),
    )
    position = models.CharField(max_length=255, choices=POSITION)
    jersey_number = models.PositiveSmallIntegerField(null=True)
    date_of_birth = models.DateField(null=True)
    nationality = models.CharField(max_length=255)
    contract_until = models.DateField(null=True)
    market_value = models.PositiveIntegerField(db_index=True, null=True)
    image = models.URLField(null=True)

    class Meta:
        ordering = ['position']

    def age(self):
        import datetime
        return int((datetime.date.today() - self.date_of_birth).days / 365.25)
