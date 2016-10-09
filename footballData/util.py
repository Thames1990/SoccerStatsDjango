import requests

from footballData.models import LeagueTable, Standing, Home, Away, LeagueID, CupID, CompetitionTypeID


def create_table(json):
    league_table, created = LeagueTable.objects.get_or_create(
        league_caption=json['leagueCaption'],
        matchday=json['matchday'],
    )
    return league_table


def create_league_table(json):
    """
    Creates a league table from JSON data.
    :param json: JSON data
    :return: LeagueTable object
    """
    league_table = create_table(json)

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


def create_cup_table(json):
    pass


def get_league_table(competiton_type_id, matchday):
    """
    Gets the league table for a specific competition on a specific matchday.
    :param competiton_type_id: ID of the requested competition type (LeagueID or CupID)
    :param matchday: The requested matchday
    :return: LeagueTable object
    """
    if isinstance(competiton_type_id, CompetitionTypeID):
        if matchday:
            if isinstance(matchday, int):
                json = requests.get(
                    'http://api.football-data.org/v1/competitions/' +
                    str(competiton_type_id.value) + '/leagueTable?matchday=' +
                    str(matchday),
                    headers={'X-Auth-Token': 'bf0513ea0ba6457fb4ae6d380cca8365'}
                ).json()
            else:
                return NotImplemented
        else:
            json = requests.get(
                'http://api.football-data.org/v1/competitions/' + str(competiton_type_id.value) + '/leagueTable',
                headers={'X-Auth-Token': 'bf0513ea0ba6457fb4ae6d380cca8365'}
            ).json()

        if isinstance(competiton_type_id, LeagueID):
            return create_league_table(json)
        elif isinstance(competiton_type_id, CupID):
            return create_cup_table(json)
    else:
        return NotImplemented


def get_league_table_position_changes(league_table, league_id=LeagueID.BL1):
    """
    Creates a list of position changes for a league table.
    :param league_table: League table of a competition
    :param league_id: ID of the leagues competition
    :return: List of position changes (True = improved, False = worsened, None = didn't change)
    """
    if isinstance(league_table, LeagueTable):
        # TODO Use _links in model to reference league_id
        # TODO Dynamically load last or second to last matchday
        league_table_last_matchday = get_league_table(league_id, league_table.matchday - 2)
        position_changes = []
        last_matchday_standing_set = league_table_last_matchday.standing_set.all()
        for standing in league_table.standing_set.all():
            last_matchday_standing = last_matchday_standing_set.get(team_name=standing.team_name)
            if standing.has_position_changed(last_matchday_standing):
                position_changes.append(standing.has_position_improved(last_matchday_standing))
            else:
                position_changes.append(None)
        return position_changes
    else:
        return NotImplemented
