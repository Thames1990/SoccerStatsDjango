import logging
import re

from competition.models import Competition
from table.models import Table, HomeStanding, AwayStanding, GroupStanding
from team.models import Team

from SoccerStats.utils import timing, rate_limited

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

    base_url = 'http://api.football-data.org/v1/competitions/' + str(competiton_id) + '/leagueTable'
    if matchday:
        base_url += '?matchday=' + str(matchday)
    return requests.get(
        url=base_url,
        headers={'X-Auth-Token': 'bf0513ea0ba6457fb4ae6d380cca8365'}
    ).json()


def create_table(table, is_cup):
    """
    Creates a table (cup or league).
    :param table: JSON representation of a cup table
    :param is_cup: *True* if *table* is a cup; *False* otherwise
    :return: List of GroupStanding objects if *table* is a cup;
    dictionary of lists of HomeStanding and AwayStanding objects otherwise
    """
    if is_cup:
        group_standings = []

        table_object = Table.objects.create(
            competition=Competition.objects.get(caption=table['leagueCaption']),
            league_caption=table['leagueCaption'],
            matchday=table['matchday'],
        )

        for cup_group in table['standings']:
            from table.models import Group
            group = Group.objects.create(
                table=table_object,
                name=cup_group,
            )

            for group_standing in table['standings'][cup_group]:
                group_standings.append(
                    GroupStanding(
                        group=group,
                        team=Team.objects.get(id=int(group_standing['teamId'])),
                        rank=group_standing['rank'],
                        played_games=group_standing['playedGames'],
                        crest_uri=group_standing['crestURI'],
                        points=group_standing['points'],
                        goals=group_standing['goals'],
                        goals_against=group_standing['goalsAgainst'],
                        goal_difference=group_standing['goalDifference'],
                    )
                )

        return group_standings
    else:
        home_standings = []
        away_standings = []

        table_object = Table.objects.create(
            competition=Competition.objects.get(caption=table['leagueCaption']),
            league_caption=table['leagueCaption'],
            matchday=table['matchday'],
        )

        for team in table['standing']:
            from table.models import Standing
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
            'home_standings': home_standings,
            'away_standings': away_standings,
        }


@timing
def create_tables():
    """Creates all tables (cups and leagues)."""
    group_standings = []
    home_standings = []
    away_standings = []

    for competition in Competition.objects.all():
        for matchday in range(1, competition.current_matchday + 1):
            table = fetch_table(competition.id, matchday)
            if 'error' not in table:
                if competition.is_cup:
                    group_standings.extend(
                        create_table(
                            table=table,
                            is_cup=True,
                        )
                    )
                else:
                    standings = create_table(
                        table=table,
                        is_cup=False,
                    )
                    home_standings.extend(standings['home_standings'])
                    away_standings.extend(standings['away_standings'])

    GroupStanding.objects.bulk_create(group_standings)
    HomeStanding.objects.bulk_create(home_standings)
    AwayStanding.objects.bulk_create(away_standings)


def update_table(table, is_cup):
    """
    Updates a table (cup or league).
    :param table: JSON representation of a table
    :param is_cup: *True*, if *table* is a cup; *False* otherwise
    """
    if is_cup:
        # DFB-Pokal doesn't have a table yet
        if 'error' not in table:
            table_object = Table.objects.get(
                competition=Competition.objects.get(caption=table['leagueCaption']),
                league_caption=table['leagueCaption'],
                matchday=table['matchday'],
            )

            for group in table['standings']:
                from table.models import Group
                group_object = Group.objects.get(
                    table=table_object,
                    name=group,
                )

                for group_standing in table['standings'][group]:
                    from table.models import GroupStanding
                    GroupStanding.objects.filter(
                        group=group_object,
                        team=Team.objects.get(id=int(group_standing['teamId']))
                    ).update(
                        rank=group_standing['rank'],
                        played_games=group_standing['playedGames'],
                        crest_uri=group_standing['crestURI'],
                        points=group_standing['points'],
                        goals=group_standing['goals'],
                        goals_against=group_standing['goalsAgainst'],
                        goal_difference=group_standing['goalDifference'],
                    )
    else:
        table_object = Table.objects.get(
            competition=Competition.objects.get(id=re.sub('[^0-9]', '', table['_links']['competition']['href'])[1:]),
            league_caption=table['leagueCaption'],
            matchday=table['matchday'],
        )

        for team in table['standing']:
            from table.models import Standing

            standing = Standing.objects.get(
                table=table_object,
                team=Team.objects.get(id=re.sub('[^0-9]', '', team['_links']['team']['href'])[1:])
            )
            standing.position = team['position']
            standing.played_games = team['playedGames']
            standing.points = team['points']
            standing.goals = team['goals']
            standing.goals_against = team['goalsAgainst']
            standing.goal_difference = team['goalDifference']
            standing.wins = team['wins']
            standing.draws = team['draws']
            standing.losses = team['losses']
            standing.save()

            HomeStanding.objects.filter(
                standing=standing
            ).update(
                goals=team['home']['goals'],
                goals_against=team['home']['goalsAgainst'],
                wins=team['home']['wins'],
                draws=team['home']['draws'],
                losses=team['home']['losses'],
            )

            AwayStanding.objects.filter(
                standing=standing
            ).update(
                goals=team['away']['goals'],
                goals_against=team['home']['goalsAgainst'],
                wins=team['away']['wins'],
                draws=team['away']['draws'],
                losses=team['away']['losses'],
            )


@timing
def update_tables():
    """Update all tables (cups and leagues)."""
    for competition in Competition.objects.all():
        current_matchday = Table.objects.filter(competition=competition).latest().matchday
        for matchday in range(current_matchday, competition.current_matchday + 1):
            table = fetch_table(competition.id, matchday)
            if matchday == competition.current_matchday:
                update_table(
                    table=table,
                    is_cup=competition.is_cup,
                )
            create_table(
                table=table,
                is_cup=competition.is_cup,
            )


def get_table_changes(table):
    """
    Calculates position/rank changes for a table (cup or league).
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
        logger.info(table.competition.caption + ' on matchday ' + str(table.matchday) +
                    ' can\'t be compared with previous matchdays')


def get_tables_current_matchday():
    """
    Get queryset of tables (cup or league) of the current matchday.
    :return: Queryset of Table objects
    """
    # TODO Change league_caption to competition.caption
    # return Table.objects.raw('''
    #         SELECT table1.id, table1.league_caption, table1.matchday
    #         FROM table_table table1, (
    #           SELECT league_caption, MAX(matchday) AS current_matchday
    #           FROM table_table
    #           GROUP BY league_caption
    #         ) AS table2
    #         WHERE table1.league_caption = table2.league_caption
    #         AND table1.matchday = table2.current_matchday
    #         ''')
    return Table.objects.all()
