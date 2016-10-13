import requests

from footballData.models import *


def create_league_table(json):
    """
    Creates a league table from JSON data.
    :param json: JSON data
    :return: LeagueTable object
    """
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


def create_cup_table(json):
    """
    Creates a cup table from JSON data.
    :param json: JSON data
    :return: CupTable object
    """
    cup_table, created = CupTable.objects.get_or_create(
        league_caption=json['leagueCaption'],
        matchday=json['matchday'],
    )

    for cup_group in json['standings']:
        group, created = Group.objects.get_or_create(
            cup_table=cup_table,
            name=cup_group,
        )

        for group_standing in json['standings'][cup_group]:
            GroupStanding.objects.get_or_create(
                group=group,
                rank=group_standing['rank'],
                team=group_standing['team'],
                team_id=group_standing['teamId'],
                played_games=group_standing['playedGames'],
                crest_uri=group_standing['crestURI'],
                points=group_standing['points'],
                goals=group_standing['goals'],
                goals_against=group_standing['goalsAgainst'],
                goal_difference=group_standing['goalDifference'],
            )

    return cup_table


def get_table(competiton_id, matchday):
    """
    Gets the league table for a specific competition on a specific matchday.
    :param competiton_id: ID of the requested competition type (LeagueID or CupID)
    :param matchday: The requested matchday
    :return: LeagueTable object
    """
    if isinstance(competiton_id, CompetitionID):
        if matchday:
            if isinstance(matchday, int):
                json = requests.get(
                    'http://api.football-data.org/v1/competitions/' +
                    str(competiton_id.value) + '/leagueTable?matchday=' +
                    str(matchday),
                    headers={'X-Auth-Token': 'bf0513ea0ba6457fb4ae6d380cca8365'}
                ).json()
            else:
                return NotImplemented
        else:
            json = requests.get(
                'http://api.football-data.org/v1/competitions/' + str(competiton_id.value) + '/leagueTable',
                headers={'X-Auth-Token': 'bf0513ea0ba6457fb4ae6d380cca8365'}
            ).json()

        if isinstance(competiton_id, LeagueID):
            return create_league_table(json)
        elif isinstance(competiton_id, CupID):
            return create_cup_table(json)
    else:
        return NotImplemented


def get_league_table_position_changes(league_table, league_id):
    """
    Creates a list of position changes for a league table.
    :param league_table: League table of a competition
    :param league_id: ID of the leagues competition
    :return: List of position changes (True = improved, False = worsened, None = didn't change)
    """
    if isinstance(league_table, LeagueTable):
        league_table_last_matchday = get_table(league_id, league_table.matchday - 2)
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


def get_cup_table_position_changes(cup_table, cup_id):
    if isinstance(cup_table, CupTable):
        cup_table_last_matchday = get_table(cup_id, cup_table.matchday - 2)
        position_changes = []
        last_matchday_group_set = cup_table_last_matchday.group_set.all()
        for group in cup_table.group_set.all():
            group_position_changes = []
            last_matchday_group = last_matchday_group_set.get(name=group.name)
            for group_standing in group.groupstanding_set.all():
                last_matchday_group_standing = last_matchday_group.groupstanding_set.get(team=group_standing.team)
                if group_standing.has_rank_changed(last_matchday_group_standing):
                    group_position_changes.append(group_standing.has_rank_improved(last_matchday_group_standing))
                else:
                    group_position_changes.append(None)
            position_changes.append(group_position_changes)
        return position_changes
    else:
        return NotImplemented
