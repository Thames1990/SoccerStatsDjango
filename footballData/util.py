import requests

from footballData.models import LeagueTable, Standing, Home, Away, LeagueID


def create_league_table(json):
    league_table, created = LeagueTable.objects.get_or_create(
        league_caption=json['leagueCaption'],
        matchday=json['matchday'],
    )

    for team in json['standing']:
        standing, created = Standing.objects.get_or_create(
            league_table=league_table,
            position=team['position'],
            team_name=team['teamName'],
            crest_uri=team['crestURI'],
            played_games=team['playedGames'],
            points=team['points'],
            goals=team['goals'],
            goals_against=team['goalsAgainst'],
            goal_difference=team['goalDifference'],
            wins=team['wins'],
            draws=team['draws'],
            losses=team['losses'],
        )

        Home.objects.get_or_create(
            standing=standing,
            goals=team['home']['goals'],
            goals_against=team['home']['goalsAgainst'],
            wins=team['home']['wins'],
            draws=team['home']['draws'],
            losses=team['home']['losses'],
        )

        Away.objects.get_or_create(
            standing=standing,
            goals=team['away']['goals'],
            goals_against=team['home']['goalsAgainst'],
            wins=team['away']['wins'],
            draws=team['away']['draws'],
            losses=team['away']['losses'],
        )

    return league_table


def get_league_table(league_id, matchday):
    if isinstance(league_id, LeagueID):
        if matchday:
            if isinstance(matchday, int):
                json = requests.get(
                    'http://api.football-data.org/v1/competitions/' +
                    str(league_id.value) + '/leagueTable?matchday=' +
                    str(matchday),
                    headers={'X-Auth-Token': 'bf0513ea0ba6457fb4ae6d380cca8365'}
                ).json()
            else:
                return NotImplemented
        else:
            json = requests.get(
                'http://api.football-data.org/v1/competitions/' + str(league_id.value) + '/leagueTable',
                headers={'X-Auth-Token': 'bf0513ea0ba6457fb4ae6d380cca8365'}
            ).json()

        return create_league_table(json)
    else:
        return NotImplemented


def get_league_table_position_changes(league_id, league_table):
    # TODO Figure out how to get league_id from the leage_table object
    if isinstance(league_table, LeagueTable):
        # TODO Dynamically load last or second to last matchday
        league_table_last_matchday = get_league_table(LeagueID.BL1, league_table.matchday - 2)
        position_changes = []
        league_table_standing = league_table.standing_set.all()
        league_table_last_matchday_standing = league_table_last_matchday.standing_set.all()
        for standing in league_table_standing:
            standing_last_matchday = league_table_last_matchday_standing.get(team_name=standing.team_name)
            if standing.has_position_changed(standing_last_matchday):
                position_changes.append(standing.has_position_improved(standing_last_matchday))
            else:
                position_changes.append(None)
        return position_changes
    else:
        return NotImplemented
