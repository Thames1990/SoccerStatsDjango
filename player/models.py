from django.db import models

from team.models import Team


class Player(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, db_index=True)
    POSITION = (
        ('Abwehr', 'Abwehr'),
        ('Attacking Midfield', 'Offensives Mittelfeld'),
        ('Central Midfield', 'Zentrales Mittelfeld'),
        ('Centre Back', 'Innenverteidiger'),
        ('Centre Forward', 'Mittelstürmer'),
        ('Defensive Midfield', 'Defensives Mittelfeld'),
        ('Defensives Mittelfeld', 'Defensives Mittelfeld'),
        ('H&auml;ngende Spitze', 'Hängende Spitze'),
        ('Innenverteidiger', 'Innenverteidiger'),
        ('Keeper', 'Torwart'),
        ('Left Midfield', 'Linkes Mittelfeld'),
        ('Left Wing', 'Linker Flügel'),
        ('Left-Back', 'Linker Außenverteidiger'),
        ('Linker Verteidiger', 'Linker Außenverteidiger'),
        ('Linksau&szlig;en', 'Linksaußen'),
        ('Midfield', 'Mittelfeld'),
        ('Mittelfeld', 'Mittelfeld'),
        ('Mittelst&uuml;rmer', 'Mittelstürmer'),
        ('Offensives Mittelfeld', 'Offensives Mittelfeld'),
        ('Rechter Verteidiger', 'Rechter Außenverteidiger'),
        ('Rechtsau&szlig;en', 'Rechtsaußen'),
        ('Right Midfield', 'Rechtes Mittelfeld'),
        ('Right Wing', 'Rechtsaußen'),
        ('Right-Back', 'Rechter Außenverteidiger'),
        ('Secondary Striker', 'Hängende Spitze'),
        ('Torwart', 'Torwart'),
        ('Zentrales Mittelfeld', 'Zentrales Mittelfeld'),
    )
    position = models.CharField(max_length=255, choices=POSITION, db_index=True)
    jersey_number = models.PositiveSmallIntegerField(null=True)
    date_of_birth = models.DateField(null=True)
    NATIONALITY = (
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
        ('Azerbaijan', 'Aserbaidschan'),
        ('Belarus', 'Weißrussland'),
        ('Belgium', 'Belgien'),
        ('Benin', 'Benin'),
        ('Bosnia-Herzegovina', 'Bosnien und Herzegowina'),
        ('Brasilien', 'Brasilien'),
        ('Brazil', 'Brasilien'),
        ('Bulgaria', 'Bulgarien'),
        ('Burkina Faso', 'Burkina Faso'),
        ('Cameroon', 'Kamerun'),
        ('Canada', 'Kanada'),
        ('Cape Verde', 'Kap Verde'),
        ('Central African Republic', 'Zentralafrikanische Republik'),
        ('Chad', 'Chad'),
        ('Chile', 'Chile'),
        ('China', 'China'),
        ('Colombia', 'Kolumbien'),
        ('Comoros', 'Komoren'),
        ('Congo', 'Kongo'),
        ('Congo DR', 'Demokratische Republik Kongo'),
        ('Costa Rica', 'Costa Rica'),
        ("Cote d'Ivoire", 'Elfenbeinküste'),
        ('Croatia', 'Kroatien'),
        ('Curacao', 'Curaçao'),
        ('Czech Republic', 'Tschechien'),
        ('Denmark', 'Dänemark'),
        ('Dominican Republic', 'Dominikanische Republik'),
        ('Ecuador', 'Ecuador'),
        ('Egypt', 'Ägypten'),
        ('El Salvador', 'El Salvador'),
        ('England', 'England'),
        ('Equatorial Guinea', 'Äquatorialguinea'),
        ('Estonia', 'Estland'),
        ('Finland', 'Finnland'),
        ('France', 'Frankreich'),
        ('Frankreich', 'Frankreich'),
        ('French Guiana', 'Französisch-Guayana'),
        ('French-Guiana', 'Französisch-Guayana'),
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
        ('Haiti', 'Haiti'),
        ('Honduras', 'Honduras'),
        ('Hungary', 'Ungarn'),
        ('Iceland', 'Island'),
        ('Iran', 'Iran'),
        ('Iraq', 'Irak'),
        ('Ireland', 'Irland'),
        ('Israel', 'Israel'),
        ('Italy', 'Italien'),
        ('Jamaica', 'Jamaika'),
        ('Japan', 'Japan'),
        ('Kazakhstan', 'Kasachstan'),
        ('Kenya', 'Kenia'),
        ('Kongo', 'Kongo'),
        ('Korea, South', 'Südkorea'),
        ('Kosovo', 'Kosovo'),
        ('Latvia', 'Lettland'),
        ('Libya', 'Lybien'),
        ('Liechtenstein', 'Liechtenstein'),
        ('Lithuania', 'Lettland'),
        ('Luxembourg', 'Luxemburg'),
        ('Macedonia', 'Mazedonien'),
        ('Madagascar', 'Madagaskar'),
        ('Mali', 'Mali'),
        ('Malta', 'Malta'),
        ('Martinique', 'Martinique'),
        ('Mauritania', 'Mauretanien'),
        ('Mexico', 'Mexiko'),
        ('Moldova', 'Moldawien'),
        ('Montenegro', 'Montenegro'),
        ('Morocco', 'Marokko'),
        ('Mozambique', 'Mosambik'),
        ('Netherlands', 'Niederlande'),
        ('Neukaledonien', 'Neukaledonien'),
        ('New Zealand', 'Neuseeland'),
        ('Nigeria', 'Nigeria'),
        ('Northern Ireland', 'Nordirland'),
        ('Norway', 'Norwegen'),
        ('Norwegen', 'Norwegen'),
        ('Palästina', 'Palästina'),
        ('Paraguay', 'Paraguay'),
        ('Peru', 'Peru'),
        ('Poland', 'Polen'),
        ('Portugal', 'Portugal'),
        ('Qatar', 'Katar'),
        ('Romania', 'Rumänien'),
        ('Russia', 'Russland'),
        ('Réunion', 'Réunion'),
        ('Saudi Arabia', 'Saudi-Arabien'),
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
        ('Thailand', 'Thailand'),
        ('The Gambia', 'Gambia'),
        ('Togo', 'Togo'),
        ('Tunisia', 'Tunesien'),
        ('Turkey', 'Turkey'),
        ('Uganda', 'Uganda'),
        ('Ukraine', 'Ukraine'),
        ('United States', 'Vereinigte Staaten'),
        ('Uruguay', 'Uruguay'),
        ('Venezuela', 'Venezuela'),
        ('Wales', 'Wales'),
        ('Zambia', 'Sambia'),
    )
    nationality = models.CharField(max_length=255, choices=NATIONALITY, db_index=True)
    contract_until = models.DateField(null=True)
    market_value = models.PositiveIntegerField(null=True)
    image = models.URLField(null=True, max_length=2000)

    class Meta:
        ordering = ['name']

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
        from SoccerStats.utils import get_wikipedia_image

        # TODO Use it
        return get_wikipedia_image('Flagge von ' + self.nationality)

    def slug(self):
        from django.utils.text import slugify

        return slugify(self.name)
