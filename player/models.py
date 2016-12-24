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
    NATION = (
        ('Poland', 'Polen'),
        ('South Africa', 'Südafrika'),
        ('Cape Verde', 'Kap Verde'),
        ('Congo', 'Kongo'),
        ('Austria', 'Österreich'),
        ('Ecuador', 'Ecuador'),
        ('Egypt', 'Ägypten'),
        ('Chile', 'Chile'),
        ('Gabon', 'Gabun'),
        ('Denmark', 'Dänemark'),
        ('Burkina Faso', 'Burkina Faso'),
        ('Netherlands', 'Niederlande'),
        ('Jamaica', 'Jamaika'),
        ('Montenegro', 'Montenegro'),
        ('Iran', 'Iran'),
        ('Portugal', 'Portugal'),
        ('Haiti', 'Haiti'),
        ('England', 'England'),
        ('United States', 'Vereinigte Staaten'),
        ('Venezuela', 'Venezuela'),
        ('Slovenia', 'Slovenien'),
        ('France', 'Frankreich'),
        ('Lithuania', 'Lettland'),
        ('Guadeloupe', 'Guadeloupe'),
        ('Ukraine', 'Ukraine'),
        ('Argentina', 'Argentinien'),
        ('Luxembourg', 'Luxemburg'),
        ('Korea, South', 'Südkorea'),
        ('Germany', 'Deutschland'),
        ('Mexico', 'Mexiko'),
        ('Croatia', 'Kroatien'),
        ('Madagascar', 'Madagaskar'),
        ('The Gambia', 'Gambia'),
        ('Brazil', 'Brasilien'),
        ('Sweden', 'Schweden'),
        ('Russia', 'Russland'),
        ('Canada', 'Kanada'),
        ('Algeria', 'Algerien'),
        ('Armenia', 'Armenien'),
        ('Belgium', 'Belgien'),
        ('Uganda', 'Uganda'),
        ('Dominican Republic', 'Dominikanische Republik'),
        ('Paraguay', 'Paraguay'),
        ('Kosovo', 'Kosovo'),
        ('Morocco', 'Marokko'),
        ('Finland', 'Finnland'),
        ('Czech Republic', 'Tschechien'),
        ('Peru', 'Peru'),
        ('Guinea', 'Guinea'),
        ('Israel', 'Israel'),
        ('Sierra Leone', 'Sierra Leone'),
        ('Latvia', 'Lettland'),
        ('Turkey', 'Turkey'),
        ('Macedonia', 'Mazedonien'),
        ('Costa Rica', 'Costa Rica'),
        ('Ireland', 'Irland'),
        ('Serbia', 'Serbien'),
        ('Slovakia', 'Slowakei'),
        ('Spain', 'Spanien'),
        ('Nigeria', 'Nigeria'),
        ('Iceland', 'Island'),
        ('Switzerland', 'Schweiz'),
        ('Italy', 'Italien'),
        ('Guine', 'Guinea'),
        ('Kenya', 'Kenia'),
        ('Australia', 'Australien'),
        ('Estonia', 'Estland'),
        ('Kazakhstan', 'Kasachstan'),
        ('Cameroon', 'Kamerun'),
        ('Senegal', 'Senegal'),
        ('Bulgaria', 'Bulgarien'),
        ('Norway', 'Norwegen'),
        ('Togo', 'Togo'),
        ('Congo DR', 'Demokratische Republik Kongo'),
        ('Antigua and Barbuda', 'Antigua und Barbuda'),
        ('Honduras', 'Honduras'),
        ('Colombia', 'Kolumbien'),
        ('Ghana', 'Ghana'),
        ('Angola', 'Angola'),
        ('Romania', 'Rumänien'),
        ('Bosnia-Herzegovina', 'Bosnien und Herzegowina'),
        ('Japan', 'Japan'),
        ('Uruguay', 'Uruguay'),
        ('Equatorial Guinea', 'Äquatorialguinea'),
        ('Greece', 'Griechenland'),
        ('Palästina', 'Palästina'),
        ('New Zealand', 'Neuseeland'),
        ('Hungary', 'Ungarn'),
        ('Tunisia', 'Tunesien'),
        ('Northern Ireland', 'Nordirland'),
        ("Cote d'Ivoire", 'Elfenbeinküste'),
        ('Georgia', 'Georgien'),
        ('Wales', 'Wales'),
        ('Curacao', 'Curaçao'),
        ('Benin', 'Benin'),
        ('Albania', 'Albanien'),
        ('Scotland', 'Schottland'),
        ('Mali', 'Mali'),
        ('Martinique', 'Martinique'),
        ('French-Guiana', 'Französisch-Guayana'),
    )
    nationality = models.CharField(max_length=255, choices=NATION)
    contract_until = models.DateField(null=True)
    market_value = models.PositiveIntegerField(db_index=True, null=True)
    image = models.URLField(null=True)

    class Meta:
        ordering = ['jersey_number']

    def __str__(self):
        return self.name + '(born in ' + self.nationality + ' on ' + str(self.date_of_birth) + \
               ') is currently playing for ' + self.team.name + ' as a ' + self.position + \
               ' and has a contract until ' + str(self.contract_until) + \
               '(Marktwert: ' + str(self.market_value) + '€).'

    def age(self):
        import datetime
        return int((datetime.date.today() - self.date_of_birth).days / 365.25)
