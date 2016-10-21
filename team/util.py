def get_or_create_competition_teams(competition_id):
    import requests
    teams = requests.get(
        'http://api.football-data.org/v1/competitions/' + str(competition_id) + '/teams',
        headers={'X-Auth-Token': 'bf0513ea0ba6457fb4ae6d380cca8365'}
    ).json()['teams']

    for team in teams:
        from team.models import Team
        import re
        return Team.objects.get_or_create(
            id=re.sub('[^0-9]', '', team['_links']['self']['href'])[1:],
            name=team['name'],
            code=team['code'] if team['code'] else None,
            short_name=team['shortName'],
            squad_market_value=re.sub('[^0-9]', '', team['squadMarketValue']) if team['squadMarketValue'] else None,
            crest_url=team['crestUrl']
        )[0]


# TODO Dafuq happens?
def get_or_create_all_teams():
    from competition.models import Competition
    competitions = []
    for competition in Competition.objects.all():
        competitions.append(get_or_create_competition_teams(competition.id))
    return competitions
