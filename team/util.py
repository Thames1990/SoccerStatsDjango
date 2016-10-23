def fetch_teams(competition_id):
    import requests

    return requests.get(
        'http://api.football-data.org/v1/competitions/' + str(competition_id) + '/teams',
        headers={'X-Auth-Token': 'bf0513ea0ba6457fb4ae6d380cca8365'}
    ).json()['teams']


def get_competition_teams(competition_id):
    teams = []
    for team in fetch_teams(competition_id):
        from competition.models import Competition
        from team.models import Team

        import re
        team = Team.objects.get_or_create(
            id=re.sub('[^0-9]', '', team['_links']['self']['href'])[1:],
            name=team['name'],
            code=team['code'] if team['code'] else None,
            short_name=team['shortName'],
            squad_market_value=re.sub('[^0-9]', '', team['squadMarketValue']) if team['squadMarketValue'] else None,
            crest_url=team['crestUrl']  # TODO Add image check and fallback download from wikipedia
        )[0]
        team.competition.add(Competition.objects.get(id=competition_id))
        teams.append(team)
    return teams


def get_all_teams():
    from competition.models import Competition

    teams = []
    for competition in Competition.objects.all():
        teams.append(get_competition_teams(competition.id))
    return teams
