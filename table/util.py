import re

from SoccerStats.util import timing, rate_limited
from competition.models import Competition, CupId, LeagueId
from table.models import CupTable, Group, GroupStanding, LeagueTable, Standing, Home, Away
from team.models import Team


# TODO Fix throttle issues (ca. 150 requests, 50 are allowed per minute)
@rate_limited(0.8)
def fetch_table(competiton_id, matchday):
    import requests

    base_url = 'http://api.football-data.org/v1/competitions/' + str(competiton_id.value) + '/leagueTable'
    if matchday:
        base_url += '?matchday=' + str(matchday)
    return requests.get(
        base_url,
        headers={'X-Auth-Token': 'bf0513ea0ba6457fb4ae6d380cca8365'}
    ).json()


def create_cup_table(table):
    groups = []
    group_standings = []

    # DFB-Pokal doesn't have a table yet
    if 'error' not in table:
        cup_table = CupTable(
            competition=Competition.objects.get(caption=table['leagueCaption']),
            matchday=table['matchday'],
        )

        for cup_group in table['standings']:
            group = Group(
                cup_table=cup_table,
                name=cup_group,
            )
            groups.append(group)

            # TODO Fix unique contraint errors
            for group_standing in table['standings'][cup_group]:
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
                group_standings.append(group_standing)

        return {
            'cup_table': cup_table,
            'groups': groups,
            'group_standings': group_standings,
        }


def create_league_table(table):
    standings = []
    home_standings = []
    away_standings = []

    try:
        Competition.objects.get(id=re.sub('[^0-9]', '', table['_links']['competition']['href'])[1:])
    except KeyError:
        print(table)

    league_table = LeagueTable(
        competition=Competition.objects.get(id=re.sub('[^0-9]', '', table['_links']['competition']['href'])[1:]),
        matchday=table['matchday'],
    )

    for team in table['standing']:
        standing = Standing(
            league_table=league_table,
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
            Home(
                standing=standing,
                goals=team['home']['goals'],
                goals_against=team['home']['goalsAgainst'],
                wins=team['home']['wins'],
                draws=team['home']['draws'],
                losses=team['home']['losses'],
            )
        )

        away_standings.append(
            Away(
                standing=standing,
                goals=team['away']['goals'],
                goals_against=team['home']['goalsAgainst'],
                wins=team['away']['wins'],
                draws=team['away']['draws'],
                losses=team['away']['losses'],
            )
        )

    return {
        'league_table': league_table,
        'standings': standings,
        'home_standings': home_standings,
        'away_standings': away_standings,
    }


@timing
def create_tables():
    cup_tables = []
    league_tables = []
    groups = []
    group_standings = []
    standings = []
    home_standings = []
    away_standings = []

    for competition in Competition.objects.all():
        for matchday in range(1, competition.current_matchday):
            try:
                competiton_id = CupId(competition.id)
                cup_table_objects = create_cup_table(fetch_table(competiton_id, matchday))
                if cup_table_objects:
                    cup_tables.append(cup_table_objects['cup_table'])
                    groups.extend(cup_table_objects['groups'])
                    group_standings.extend(cup_table_objects['group_standings'])
            except ValueError:
                competiton_id = LeagueId(competition.id)
                league_table_objects = create_league_table(fetch_table(competiton_id, matchday))
                league_tables.append(league_table_objects['league_table'])
                standings.extend(league_table_objects['standings'])
                home_standings.extend(league_table_objects['home_standings'])
                away_standings.extend(league_table_objects['away_standings'])

    CupTable.objects.bulk_create(cup_tables)
    LeagueTable.objects.bulk_create(league_tables)
    Group.objects.bulk_create(groups)
    GroupStanding.objects.bulk_create(group_standings)
    Standing.objects.bulk_create(standings)
    Home.objects.bulk_create(home_standings)
    Away.objects.bulk_create(away_standings)


def get_cup_table_position_changes(cup_table):
    cup_table = CupTable.objects.get(id=cup_table.id)
    try:
        cup_table_last_matchday = CupTable.objects.get(
            competition=cup_table.competition,
            league_caption=cup_table.league_caption,
            matchday=cup_table.matchday - 1,
        )

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
    except CupTable.DoesNotExist:
        # TODO log
        pass


def get_league_table_position_changes(league_table):
    league_table = LeagueTable.objects.get(id=league_table.id)
    try:
        league_table_last_matchday = LeagueTable.objects.get(
            competition=league_table.competition,
            league_caption=league_table.league_caption,
            matchday=league_table.matchday - 1,
        )

        position_changes = []
        last_matchday_standing_set = league_table_last_matchday.standing_set.all()
        for standing in league_table.standing_set.all():
            last_matchday_standing = last_matchday_standing_set.get(team__name=standing.team.name)
            if standing.has_position_changed(last_matchday_standing):
                position_changes.append(standing.has_position_improved(last_matchday_standing))
            else:
                position_changes.append(None)
        return position_changes
    except LeagueTable.DoesNotExist:
        # TODO log
        pass
