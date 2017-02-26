import logging
import os
import re

from SoccerStats.utils import timing, rate_limited
from competition.models import Competition
from table.models import Table, Group, GroupStanding, Standing, HomeStanding, AwayStanding
from team.models import Team

logger = logging.getLogger(__name__)


@rate_limited(0.8)
def fetch_table(competiton_id, matchday=None):
    """
    Fetches football-data.org JSON representation of a table from a competition with *competition_id* on a specific
    *matchday*.
    :param competiton_id: Id of a competition
    :param matchday: Matchday of a competition
    :return: JSON representation of a table from a competition with *competition_id* on a specific *matchday*
    """
    import requests

    base_url = 'https://api.football-data.org/v1/competitions/' + str(competiton_id) + '/leagueTable'
    if matchday:
        base_url += '?matchday=' + str(matchday)
    return requests.get(
        url=base_url,
        headers={'X-Auth-Token': os.environ['X_AUTH_TOKEN']},
    ).json()


def create_cup_table(table):
    """
    Creates a cup table.
    :param table: JSON representation of a table
    :return: List of GroupStanding objects
    """
    groups = []
    group_standings = []

    table_object = Table.objects.create(
        competition=Competition.objects.get(caption=table['leagueCaption']),
        matchday=table['matchday'],
    )

    for cup_group in table['standings']:
        group = Group.objects.create(
            table=table_object,
            name=cup_group,
        )
        groups.append(group)

        for group_standing in table['standings'][cup_group]:
            group_standings.append(
                GroupStanding(
                    group=group,
                    team=Team.objects.get(id=group_standing['teamId']),
                    rank=group_standing['rank'],
                    played_games=group_standing['playedGames'],
                    crest_uri=group_standing['crestURI'],
                    points=group_standing['points'],
                    goals=group_standing['goals'],
                    goals_against=group_standing['goalsAgainst'],
                    goal_difference=group_standing['goalDifference'],
                )
            )

    return {
        'table_object': table_object,
        'groups': groups,
        'group_standings': group_standings,
    }


def create_league_table(table):
    """
    Creates a league table.
    :param table: JSON representation of a table
    :return: Dictionary of lists of HomeStanding and AwayStanding objects
    """
    table_object = Table.objects.create(
        competition=Competition.objects.get(caption=table['leagueCaption']),
        matchday=table['matchday'],
    )

    standings = []
    home_standings = []
    away_standings = []

    for team in table['standing']:
        standing = Standing.objects.create(
            table=table_object,
            position=team['position'],
            team=Team.objects.get(id=re.sub('[^0-9]', '', team['_links']['team']['href'])[1:]),
            played_games=team['playedGames'],
            points=team['points'],
            goals=team['goals'],
            goals_against=team['goalsAgainst'],
            goal_difference=team['goalDifference'],
            wins=team['wins'],
            draws=team['draws'],
            losses=team['losses'],
        )
        standings.append(standing)

        home_standings.append(
            HomeStanding(
                standing=standing,
                goals=team['home']['goals'],
                goals_against=team['home']['goalsAgainst'],
                wins=team['home']['wins'],
                draws=team['home']['draws'],
                losses=team['home']['losses'],
            )
        )

        away_standings.append(
            AwayStanding(
                standing=standing,
                goals=team['away']['goals'],
                goals_against=team['home']['goalsAgainst'],
                wins=team['away']['wins'],
                draws=team['away']['draws'],
                losses=team['away']['losses'],
            )
        )

    return {
        'table_object': table_object,
        'standings': standings,
        'home_standings': home_standings,
        'away_standings': away_standings,
    }


def create_table(table, is_cup):
    """
    Creates a table.
    :param table: JSON representation of a table
    :param is_cup: *True* if *table* is a cup; *False* otherwise
    :return: List of GroupStanding objects if *table* is a cup;
    dictionary of lists of HomeStanding and AwayStanding objects otherwise
    """
    if is_cup:
        return create_cup_table(table)
    else:
        return create_league_table(table)


@timing
def create_tables():
    """
    Creates all tables.
    :return: Dictionary of created tables, groups, group standings, standings, home standings and away standings
    """
    logger.info('Creating tables...')

    created_tables = []
    created_groups = []
    group_standings = []
    created_standings = []
    home_standings = []
    away_standings = []

    for competition in Competition.objects.all():
        for matchday in range(1, competition.current_matchday + 1):
            table = fetch_table(competition.id, matchday)
            if 'error' not in table:
                table_object = create_table(
                    table=table,
                    is_cup=competition.is_cup,
                )
                if competition.is_cup:
                    created_tables.append(table_object['table_object'])
                    created_groups.extend(table_object['groups'])
                    group_standings.extend(table_object['group_standings'])
                else:
                    created_tables.append(table_object['table_object'])
                    created_standings.append(table_object['standings'])
                    home_standings.extend(table_object['home_standings'])
                    away_standings.extend(table_object['away_standings'])

    created_group_standings = GroupStanding.objects.bulk_create(group_standings)
    created_home_standings = HomeStanding.objects.bulk_create(home_standings)
    created_away_standings = AwayStanding.objects.bulk_create(away_standings)

    logger.info('Created ' + str(len(created_tables)) + ' tables')
    logger.info('Created ' + str(len(created_groups)) + ' groups')
    logger.info('Created ' + str(len(created_group_standings)) + ' group standings')
    logger.info('Created ' + str(len(created_standings)) + ' standings')
    logger.info('Created ' + str(len(created_home_standings)) + ' home standings')
    logger.info('Created ' + str(len(created_away_standings)) + ' away standings')

    return {
        'tables': created_tables,
        'groups': created_groups,
        'created_group_standings': created_group_standings,
        'standings': created_standings,
        'created_home_standings': created_home_standings,
        'created_away_standings': created_away_standings,
    }


def update_or_create_group_standing(group_object, group_standing):
    """
    Updates or creates a group standing.
    :param group_object: Linked group
    :param group_standing: JSON representing the group standing
    :return: Updated or created group standing and *True*, if the group standing was created; *False* otherwise
    """
    return GroupStanding.objects.update_or_create(
        group=group_object,
        team=Team.objects.get(id=group_standing['teamId']),
        defaults={
            'group': group_object,
            'team': Team.objects.get(id=group_standing['teamId']),
            'rank': group_standing['rank'],
            'played_games': group_standing['playedGames'],
            'crest_uri': group_standing['crestURI'],
            'points': group_standing['points'],
            'goals': group_standing['goals'],
            'goals_against': group_standing['goalsAgainst'],
            'goal_difference': group_standing['goalDifference'],
        }
    )


def update_cup_table(table):
    """
    Updates a cup table.
    :param table: JSON representation of a table
    """
    updated_group_standings = []
    created_group_standings = 0

    # DFB-Pokal doesn't have a table yet
    if 'error' not in table:
        table_object = Table.objects.get(
            competition=Competition.objects.get(caption=table['leagueCaption']),
            matchday=table['matchday'],
        )

        for group in table['standings']:
            group_object = Group.objects.get(
                table=table_object,
                name=group,
            )

            for group_standing in table['standings'][group]:
                group_standing_object, created = update_or_create_group_standing(
                    group_object=group_object,
                    group_standing=group_standing,
                )

                created_group_standings += 1 if created else updated_group_standings.append(group_standing_object)

        return {
            'updated_group_standings': updated_group_standings,
            'created_group_standings': created_group_standings,
        }


def update_or_create_standing(table_object, team):
    """
    Updates or creates a standing.
    :param table_object: Linked table
    :param team: Linked team
    :return: Updated or created standing and *True*, if the standing was created; *False* otherwise
    """
    return Standing.objects.update_or_create(
        table=table_object,
        team=Team.objects.get(id=re.sub('[^0-9]', '', team['_links']['team']['href'])[1:]),
        defaults={
            'table': table_object,
            'team': Team.objects.get(id=re.sub('[^0-9]', '', team['_links']['team']['href'])[1:]),
            'position': team['position'],
            'played_games': team['playedGames'],
            'points': team['points'],
            'goals': team['goals'],
            'goals_against': team['goalsAgainst'],
            'goal_difference': team['goalDifference'],
            'wins': team['wins'],
            'draws': team['draws'],
            'losses': team['losses'],
        }
    )


def update_or_create_home_standing(standing, team):
    """
    Updates or creates an home standing.
    :param standing: Linked standing
    :param team: Linked team
    :return: Updated or created home standing and *True*, if the home standing was created; *False* otherwise
    """
    return HomeStanding.objects.update_or_create(
        standing=standing,
        defaults={
            'standing': standing,
            'goals': team['home']['goals'],
            'goals_against': team['home']['goalsAgainst'],
            'wins': team['home']['wins'],
            'draws': team['home']['draws'],
            'losses': team['home']['losses'],
        }
    )


def update_or_create_away_standing(standing, team):
    """
    Updates or creates an away standing.
    :param standing: Linked standing
    :param team: Linked team
    :return: Updated or created away standing and *True*, if the away standing was created; *False* otherwise
    """
    return AwayStanding.objects.update_or_create(
        standing=standing,
        defaults={
            'standing': standing,
            'goals': team['away']['goals'],
            'goals_against': team['home']['goalsAgainst'],
            'wins': team['away']['wins'],
            'draws': team['away']['draws'],
            'losses': team['away']['losses'],
        }
    )


def update_league_table(table):
    """
    Updates a league table.
    :param table: JSON representation of a table
    """
    updated_standings = []
    created_standings = 0
    updated_home_standings = []
    created_home_standings = 0
    updated_away_standings = []
    created_away_standings = 0

    table_object = Table.objects.get(
        competition=Competition.objects.get(id=re.sub('[^0-9]', '', table['_links']['competition']['href'])[1:]),
        matchday=table['matchday'],
    )

    for team in table['standing']:
        standing, created = update_or_create_standing(table_object=table_object, team=team)

        if created:
            created_standings += 1
        else:
            updated_standings.append(standing)

        home_standing, created = update_or_create_home_standing(standing=standing, team=team)

        if created:
            created_home_standings += 1
        else:
            updated_home_standings.append(home_standing)

        away_standing, created = update_or_create_away_standing(standing=standing, team=team)

        if created:
            created_away_standings += 1
        else:
            updated_away_standings.append(away_standing)

    return {
        'updated_standings': updated_standings,
        'created_standings': created_standings,
        'updated_home_standings': updated_home_standings,
        'created_home_standings': created_home_standings,
        'updated_away_standings': updated_away_standings,
        'created_away_standings': created_away_standings,
    }


def update_table(table, is_cup):
    """
    Updates a table.
    :param table: JSON representation of a table
    :param is_cup: *True*, if *table* is a cup; *False* otherwise
    """
    if is_cup:
        return update_cup_table(table)
    else:
        return update_league_table(table)


@timing
def update_tables():
    """
    Updates all tables.
    :return: Dictionary of updated group standings, standings, home standings and away standings
    """
    logger.info('Updating tables...')

    created_tables = 0
    created_groups = 0
    updated_group_standings = []
    created_group_standings = 0
    updated_standings = []
    created_standings = 0
    updated_home_standings = []
    created_home_standings = 0
    updated_away_standings = []
    created_away_standings = 0

    for competition in Competition.objects.all():
        if Table.objects.filter(competition=competition).exists():
            current_matchday = Table.objects.filter(competition=competition).latest().matchday
            for matchday in range(current_matchday, competition.current_matchday + 1):
                table = fetch_table(competition.id, matchday)
                # DFB Pokal and Champions League with less specified matchdays than set in numberOfMatchdays
                if 'error' not in table and '_links' in table:
                    # Current matchday that exists
                    if matchday == competition.current_matchday and Table.objects.filter(
                            competition=Competition.objects.get(
                                id=re.sub('[^0-9]', '', table['_links']['competition']['href'])[1:]
                            ),
                            matchday=table['matchday'],
                    ).exists():
                        table_object = update_table(
                            table=table,
                            is_cup=competition.is_cup,
                        )

                        if competition.is_cup:
                            updated_group_standings.extend(table_object['updated_group_standings'])
                            created_group_standings.extend(table_object['created_group_standings'])
                        else:
                            updated_standings.extend(table_object['updated_standings'])
                            created_standings += table_object['created_standings']
                            updated_home_standings.extend(table_object['updated_home_standings'])
                            created_home_standings += table_object['created_home_standings']
                            updated_away_standings.extend(table_object['updated_away_standings'])
                            created_away_standings += table_object['created_away_standings']
                    # Current matchday that doesn't exist. Prevents duplicates.
                    elif not Table.objects.filter(
                            competition=Competition.objects.get(
                                id=re.sub('[^0-9]', '', table['_links']['competition']['href'])[1:]
                            ),
                            matchday=table['matchday'],
                    ).exists():
                        table_object = create_table(
                            table=table,
                            is_cup=competition.is_cup,
                        )

                        if competition.is_cup:
                            created_tables += 1
                            created_groups += len(table_object['groups'])
                            created_group_standings += len(table_object['group_standings'])
                        else:
                            created_tables += 1
                            created_standings += len(table_object['standings'])
                            created_home_standings += len(table_object['home_standings'])
                            created_away_standings += len(table_object['away_standings'])
                    else:
                        # Shouldn't happen!
                        logger.warning('I might think about the table update process')

    logger.info('Created ' + str(created_tables) + ' tables')
    logger.info('Created ' + str(created_groups) + ' groups')
    logger.info(
        'Updated ' + str(len(updated_group_standings)) + ' group standings, created ' + str(created_group_standings)
    )
    logger.info(
        'Updated ' + str(len(updated_standings)) + ' group standings, created ' + str(created_standings)
    )
    logger.info(
        'Updated ' + str(len(updated_home_standings)) + ' group standings, created ' + str(created_home_standings)
    )
    logger.info(
        'Updated ' + str(len(updated_away_standings)) + ' group standings, created ' + str(created_away_standings)
    )

    return {
        'updated_group_standings': updated_group_standings,
        'updated_standings': updated_standings,
        'updated_home_standings': updated_home_standings,
        'updated_away_standings': updated_away_standings,
    }


def get_table_changes(table):
    """
    Calculates position/rank changes for a table.
    :param table: Table to calculate position/rank changes for
    :return: List of position changes
    """
    if table.matchday > 1:
        table_last_matchday = Table.objects.get(
            competition=table.competition,
            matchday=table.matchday - 1,
        )

        if table.competition.is_cup:
            rank_changes = []
            last_matchday_group_set = table_last_matchday.group_set.all()
            for group in table.group_set.all():
                group_rank_changes = []
                last_matchday_group = last_matchday_group_set.get(name=group.name)
                for group_standing in group.groupstanding_set.all():
                    last_matchday_group_standing = last_matchday_group.groupstanding_set.get(team=group_standing.team)
                    if group_standing.has_rank_changed(last_matchday_group_standing):
                        group_rank_changes.append(group_standing.has_rank_improved(last_matchday_group_standing))
                    else:
                        group_rank_changes.append(None)
                rank_changes.append(group_rank_changes)
            return rank_changes
        else:
            position_changes = []
            last_matchday_standing_set = table_last_matchday.standing_set.all()
            for standing in table.standing_set.all():
                last_matchday_standing = last_matchday_standing_set.get(team__name=standing.team.name)
                if standing.has_position_changed(last_matchday_standing):
                    position_changes.append(standing.has_position_improved(last_matchday_standing))
                else:
                    position_changes.append(None)
            return position_changes
    else:
        logger.warning(
            table.competition.caption + ' on matchday ' +
            str(table.matchday) + ' can\'t be compared with previous matchdays'
        )


def get_tables_current_matchday():
    """
    Get queryset of tables of the current matchday.
    :return: Queryset of Table objects
    """
    from django.db.models import Max, Q
    current_matchday_tables = \
        Table.objects.values('competition__caption').annotate(current_matchday=Max('matchday'))
    q_statement = Q()
    for current_matchday_table in current_matchday_tables:
        q_statement |= (
            Q(competition__caption=current_matchday_table['competition__caption']) &
            Q(matchday=current_matchday_table['current_matchday'])
        )
    return Table.objects.filter(q_statement)


def get_records():
    """
    Calculates the records for scored/conceded goals and points for all competitions.
    :return: Dictionary of records
    """
    from django.db.models import Max

    tables = Table.objects.all()
    return {
        'goals': tables.aggregate(Max('standing__goals'))['standing__goals__max'],
        'goals_against': tables.aggregate(Max('standing__goals_against'))['standing__goals_against__max'],
        'points': tables.aggregate(Max('standing__points'))['standing__points__max'],
    }
