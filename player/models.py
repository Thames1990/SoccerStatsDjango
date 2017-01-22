from django.db import models

from team.models import Team


class Player(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, db_index=True)
    POSITION = (
        # Goalkeeper
        ('Keeper', 'Torwart'),
        ('Torwart', 'Torwart'),
        # Defender
        ('Abwehr', 'Abwehr'),
        ('Left-Back', 'Linker Außenverteidiger'),
        ('Linker Verteidiger', 'Linker Verteidiger'),
        ('Centre Back', 'Innenverteidiger'),
        ('Innenverteidiger', 'Innenverteidiger'),
        ('Right-Back', 'Rechter Außenverteidiger'),
        ('Rechter Verteidiger', 'Rechter Verteidiger'),
        # Midfielder
        ('Midfield', 'Mittelfeld'),
        ('Mittelfeld', 'Mittelfeld'),
        ('Defensive Midfield', 'Defensives Mittelfeld'),
        ('Defensives Mittelfeld', 'Defensives Mittelfeld'),
        ('Left Midfield', 'Linkes Mittelfeld'),
        ('Central Midfield', 'Zentrales Mittelfeld'),
        ('Zentrales Mittelfeld', 'Zentrales Mittelfeld'),
        ('Right Midfield', 'Rechtes Mittelfeld'),
        ('Attacking Midfield', 'Offensives Mittelfeld'),
        ('Offensives Mittelfeld', 'Offensives Mittelfeld'),
        # Forward
        ('Linksau&szlig;en', 'Linksaußen'),
        ('Left Wing', 'Linker Flügel'),
        ('Secondary Striker', 'Hängende Spitze'),
        ('H&auml;ngende Spitze', 'Hängende Spitze'),
        ('Centre Forward', 'Stürmer'),
        ('Mittelst&uuml;rmer', 'Mittelstürmer'),
        ('Right Wing', 'Rechter Flügel'),
        ('Rechtsau&szlig;en', 'Rechtsaußen'),
    )
    position = models.CharField(max_length=255, choices=POSITION)
    jersey_number = models.PositiveSmallIntegerField(null=True)
    date_of_birth = models.DateField(null=True)
    NATIONALITY = (
        # A
        ('Albania', 'Albanien'),
        ('Albanien', 'Albanien'),
        ('Algeria', 'Algerien'),
        ('Angola', 'Angola'),
        ('Antigua and Barbuda', 'Antigua und Barbuda'),
        ('Argentina', 'Argentinien'),
        ('Argentinien', 'Argentinien'),
        ('Armenia', 'Armenien'),
        ('Australia', 'Australien'),
        ('Austria', 'Österreich'),
        # B
        ('Belarus', 'Weißrussland'),
        ('Belgium', 'Belgien'),
        ('Benin', 'Benin'),
        ('Bosnia-Herzegovina', 'Bosnien und Herzegowina'),
        ('Brasilien', 'Brasilien'),
        ('Brazil', 'Brasilien'),
        ('Bulgaria', 'Bulgarien'),
        ('Burkina Faso', 'Burkina Faso'),
        # C
        ('Cameroon', 'Kamerun'),
        ('Canada', 'Kanada'),
        ('Cape Verde', 'Kap Verde'),
        ('Central African Republic', 'Zentralafrikanische Republik'),
        ('Chile', 'Chile'),
        ('Colombia', 'Kolumbien'),
        ('Congo', 'Kongo'),
        ('Congo DR', 'Demokratische Republik Kongo'),
        ('Costa Rica', 'Costa Rica'),
        ("Cote d'Ivoire", 'Elfenbeinküste'),
        ('Croatia', 'Kroatien'),
        ('Curacao', 'Curaçao'),
        ('Czech Republic', 'Tschechien'),
        # D
        ('Denmark', 'Dänemark'),
        ('Dominican Republic', 'Dominikanische Republik'),
        # E
        ('Ecuador', 'Ecuador'),
        ('Egypt', 'Ägypten'),
        ('England', 'England'),
        ('Estonia', 'Estland'),
        ('Equatorial Guinea', 'Äquatorialguinea'),
        # F
        ('Finland', 'Finnland'),
        ('France', 'Frankreich'),
        ('Frankreich', 'Frankreich'),
        ('French-Guiana', 'Französisch-Guayana'),
        # G
        ('Gabon', 'Gabun'),
        ('Georgia', 'Georgien'),
        ('Germany', 'Deutschland'),
        ('Ghana', 'Ghana'),
        ('Greece', 'Griechenland'),
        ('Griechenland', 'Griechenland'),
        ('Guadeloupe', 'Guadeloupe'),
        ('Guine', 'Guinea'),
        ('Guinea', 'Guinea'),
        ('Guinea-Bissau', 'Guinea-Bissau'),
        # H
        ('Haiti', 'Haiti'),
        ('Honduras', 'Honduras'),
        ('Hungary', 'Ungarn'),
        # I
        ('Iceland', 'Island'),
        ('Iran', 'Iran'),
        ('Iraq', 'Irak'),
        ('Ireland', 'Irland'),
        ('Israel', 'Israel'),
        ('Italy', 'Italien'),
        # J
        ('Jamaica', 'Jamaika'),
        ('Japan', 'Japan'),
        # K
        ('Kazakhstan', 'Kasachstan'),
        ('Kenya', 'Kenia'),
        ('Kongo', 'Kongo'),
        ('Korea, South', 'Südkorea'),
        ('Kosovo', 'Kosovo'),
        # L
        ('Latvia', 'Lettland'),
        ('Libya', 'Lybien'),
        ('Liechtenstein', 'Liechtenstein'),
        ('Lithuania', 'Lettland'),
        ('Luxembourg', 'Luxemburg'),
        # M
        ('Macedonia', 'Mazedonien'),
        ('Madagascar', 'Madagaskar'),
        ('Mali', 'Mali'),
        ('Martinique', 'Martinique'),
        ('Mexico', 'Mexiko'),
        ('Montenegro', 'Montenegro'),
        ('Morocco', 'Marokko'),
        # N
        ('Netherlands', 'Niederlande'),
        ('New Zealand', 'Neuseeland'),
        ('Nigeria', 'Nigeria'),
        ('Northern Ireland', 'Nordirland'),
        ('Norway', 'Norwegen'),
        ('Norwegen', 'Norwegen'),
        # P
        ('Palästina', 'Palästina'),
        ('Paraguay', 'Paraguay'),
        ('Peru', 'Peru'),
        ('Poland', 'Polen'),
        ('Portugal', 'Portugal'),
        # R
        ('Romania', 'Rumänien'),
        ('Russia', 'Russland'),
        # S
        ('Schweiz', 'Schweiz'),
        ('Scotland', 'Schottland'),
        ('Senegal', 'Senegal'),
        ('Serbia', 'Serbien'),
        ('Serbien', 'Serbien'),
        ('Sierra Leone', 'Sierra Leone'),
        ('Slovakia', 'Slowakei'),
        ('Slovenia', 'Slovenien'),
        ('South Africa', 'Südafrika'),
        ('Spain', 'Spanien'),
        ('Spanien', 'Spanien'),
        ('Sweden', 'Schweden'),
        ('Switzerland', 'Schweiz'),
        # T
        ('Thailand', 'Thailand'),
        ('The Gambia', 'Gambia'),
        ('Togo', 'Togo'),
        ('Tunisia', 'Tunesien'),
        ('Turkey', 'Turkey'),
        # U
        ('Uganda', 'Uganda'),
        ('Ukraine', 'Ukraine'),
        ('United States', 'Vereinigte Staaten'),
        ('Uruguay', 'Uruguay'),
        # V
        ('Venezuela', 'Venezuela'),
        # W
        ('Wales', 'Wales'),
    )
    nationality = models.CharField(max_length=255, choices=NATIONALITY)
    contract_until = models.DateField(null=True)
    market_value = models.PositiveIntegerField(null=True)
    image = models.URLField(null=True, max_length=2000)

    class Meta:
        ordering = ['jersey_number']

    def __str__(self):
        return '%s playing for %s' % (
            self.name,
            self.team.name,
        )

    def age(self):
        if self.date_of_birth:
            import datetime
            return int((datetime.date.today() - self.date_of_birth).days / 365.25)
        else:
            return None

    def get_nationality_flag(self):
        from player.utils import get_wikipedia_image
        return get_wikipedia_image('Flagge von ' + self.nationality)
