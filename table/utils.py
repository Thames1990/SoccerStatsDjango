from SoccerStats.utils import timing
from competition.models import Competition, CupId, LeagueId
from table.models import CupTable, LeagueTable, Home, Away
from team.models import Team


def create_cup_table(json):
    # DFB-Pokal doesn't have a table yet
    if 'error' not in json:
        cup_table = CupTable.objects.create(
            competition=Competition.objects.get(caption=json['leagueCaption']),
            league_caption=json['leagueCaption'],
            matchday=json['matchday'],
        )

        for cup_group in json['standings']:
            from table.models import Group
            group = Group.objects.create(
                cup_table=cup_table,
                name=cup_group,
            )

            for group_standing in json['standings'][cup_group]:
                from table.models import GroupStanding
                GroupStanding.objects.create(
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


def create_league_table(json):
    import re
    league_table = LeagueTable.objects.create(
        competition=Competition.objects.get(id=re.sub('[^0-9]', '', json['_links']['competition']['href'])[1:]),
        league_caption=json['leagueCaption'],
        matchday=json['matchday'],
    )

    for team in json['standing']:
        from table.models import Standing
        standing = Standing.objects.create(
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

        Home.objects.create(
            standing=standing,
            goals=team['home']['goals'],
            goals_against=team['home']['goalsAgainst'],
            wins=team['home']['wins'],
            draws=team['home']['draws'],
            losses=team['home']['losses'],
        )

        Away.objects.create(
            standing=standing,
            goals=team['away']['goals'],
            goals_against=team['home']['goalsAgainst'],
            wins=team['away']['wins'],
            draws=team['away']['draws'],
            losses=team['away']['losses'],
        )


def create_table(competiton_id, matchday=None):
    import requests

    base_url = 'http://api.football-data.org/v1/competitions/' + str(competiton_id.value) + '/leagueTable'
    if matchday:
        base_url += '?matchday=' + str(matchday)
    json = requests.get(
        base_url,
        headers={'X-Auth-Token': 'bf0513ea0ba6457fb4ae6d380cca8365'}
    ).json()
    if isinstance(competiton_id, CupId):
        create_cup_table(json)
    elif isinstance(competiton_id, LeagueId):
        create_league_table(json)


@timing
def create_all_tables():
    from competition.utils import fetch_competitions

    for competition in fetch_competitions():
        competition = Competition.objects.get(id=competition['id'])
        for matchday in range(1, competition.current_matchday):
            try:
                competiton_id = CupId(competition.id)
            except ValueError:
                competiton_id = LeagueId(competition.id)

            create_table(competiton_id, matchday)


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
        pass


def get_cup_table_current_matchday():
    return CupTable.objects.raw('''
            SELECT cup_table1.id, cup_table1.league_caption, cup_table1.matchday
            FROM table_cuptable cup_table1, (
              SELECT league_caption, MAX(matchday) AS current_matchday
              FROM table_cuptable
              GROUP BY league_caption
            ) AS cup_table2
            WHERE cup_table1.league_caption = cup_table2.league_caption
            AND cup_table1.matchday = cup_table2.current_matchday
            ''')


def get_league_table_current_matchday():
    return LeagueTable.objects.raw('''
            SELECT league_table1.id, league_table1.league_caption, league_table1.matchday
            FROM table_leaguetable league_table1, (
              SELECT league_caption, MAX(matchday) AS current_matchday
              FROM table_leaguetable
              GROUP BY league_caption
            ) AS league_table2
            WHERE league_table1.league_caption = league_table2.league_caption
            AND league_table1.matchday = league_table2.current_matchday
            ''')


def get_group_standing_average_goals(cup_tables_current_matchday):
    return sum(groupstanding.goals for groupstanding in
               (group.groupstanding_set.all() for group in
                (cup_table.group_set.all() for cup_table in
                 cup_tables_current_matchday))) / len(list(cup_tables_current_matchday))


def get_standing_average_goals(league_tables_current_matchday):
    return sum(standing.goals for standing in
               (league_table.standing_set.all() for league_table in
                league_tables_current_matchday)) / len(list(league_tables_current_matchday))
