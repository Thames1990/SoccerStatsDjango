import re

from competition.models import Competition, CupId, LeagueId
from table.models import CupTable, LeagueTable, Home, Away
from team.models import Team

from SoccerStats.utils import timing
from competition.utils import fetch_competitions


def fetch_tables(competiton_id, matchday):
    """
    Fetches football-data.org JSON representation of a table from a competition with *competition_id* on a specific
    *matchday*.
    :param competiton_id: Id of a competition
    :param matchday: Matchday of a competition
    :return: JSON representation of a table from a competition with *competition_id* on a specific *matchday*
    """
    import requests

    base_url = 'http://api.football-data.org/v1/competitions/' + str(competiton_id.value) + '/leagueTable'
    if matchday:
        base_url += '?matchday=' + str(matchday)
    return requests.get(
        base_url,
        headers={'X-Auth-Token': 'bf0513ea0ba6457fb4ae6d380cca8365'}
    ).json()


def create_cup_table(table):
    """
    Creates a CupTable from the JSON encoded representation *table*.
    :param table: JSON representation of a cup table
    """
    # DFB-Pokal doesn't have a table yet
    if 'error' not in table:
        cup_table = CupTable.objects.create(
            competition=Competition.objects.get(caption=table['leagueCaption']),
            league_caption=table['leagueCaption'],
            matchday=table['matchday'],
        )

        for cup_group in table['standings']:
            from table.models import Group
            group = Group.objects.create(
                cup_table=cup_table,
                name=cup_group,
            )

            for group_standing in table['standings'][cup_group]:
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


def create_league_table(table):
    """
    Creates a LeagueTable.
    :param table: JSON representation of a cup table
    """
    league_table = LeagueTable.objects.create(
        competition=Competition.objects.get(id=re.sub('[^0-9]', '', table['_links']['competition']['href'])[1:]),
        league_caption=table['leagueCaption'],
        matchday=table['matchday'],
    )

    for team in table['standing']:
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


@timing
def create_tables():
    """
    Creates all tables (CupTable and LeagueTable).
    """
    # TODO Rewrite with bulk_create
    for competition in fetch_competitions():
        competition = Competition.objects.get(id=competition['id'])
        for matchday in range(1, competition.current_matchday + 1):
            try:
                create_cup_table(fetch_tables(CupId(competition.id), matchday))
            except ValueError:
                create_league_table(fetch_tables(LeagueId(competition.id), matchday))


def update_cup_table(table):
    """
    Updates a cup table.
    :param table: JSON representation of a cup table
    :return:
    """
    if 'error' not in table:
        cup_table = CupTable.objects.get(
            competition=Competition.objects.get(caption=table['leagueCaption']),
            league_caption=table['leagueCaption'],
            matchday=table['matchday'],
        )

        for cup_group in table['standings']:
            from table.models import Group
            group = Group.objects.get(
                cup_table=cup_table,
                name=cup_group,
            )

            for group_standing in table['standings'][cup_group]:
                from table.models import GroupStanding
                GroupStanding.objects.filter(
                    group=group,
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


def update_league_table(table):
    """
    Updates a league table.
    :param table: JSON representation of a league table
    :return:
    """
    league_table = LeagueTable.objects.get(
        competition=Competition.objects.get(id=re.sub('[^0-9]', '', table['_links']['competition']['href'])[1:]),
        league_caption=table['leagueCaption'],
        matchday=table['matchday'],
    )

    for team in table['standing']:
        from table.models import Standing
        standing = Standing.objects.get(
            league_table=league_table,
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

        Home.objects.filter(standing=standing).update(
            goals=team['home']['goals'],
            goals_against=team['home']['goalsAgainst'],
            wins=team['home']['wins'],
            draws=team['home']['draws'],
            losses=team['home']['losses'],
        )

        Away.objects.filter(standing=standing).update(
            goals=team['away']['goals'],
            goals_against=team['home']['goalsAgainst'],
            wins=team['away']['wins'],
            draws=team['away']['draws'],
            losses=team['away']['losses'],
        )


@timing
def update_tables():
    """
    Update all tables (CupTable, LeagueTable).
    :return:
    """
    for competition in fetch_competitions():
        # TODO Fix this shit
        current_matchday = 1
        competition_object = Competition.objects.get(id=competition['id'])
        try:
            current_matchday = LeagueTable.objects.filter(competition=competition_object).latest().matchday
        except LeagueTable.DoesNotExist:
            print(competition_object.id)
            try:
                current_matchday = CupTable.objects.filter(competition=competition_object).latest().matchday
            except CupTable.DoesNotExist:
                print(competition_object.id)

        for matchday in range(current_matchday, competition['currentMatchday'] + 1):
            try:
                table = fetch_tables(CupId(competition['id']), matchday)
                if matchday == competition['currentMatchday']:
                    update_cup_table(table)
                create_cup_table(table)
            except ValueError:
                table = fetch_tables(LeagueId(competition['id']), matchday)
                if matchday == competition['currentMatchday']:
                    update_league_table(table)
                create_league_table(table)


def get_cup_table_rank_changes(cup_table):
    """
    Calculates rank changes in a cup table.
    :param cup_table: Cup table to calculate the rank changes for
    :return: List of rank changes
    """
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
    """
    Calculates position changes for a league table.
    :param league_table: League table to calculate position changes for
    :return: List of position changes
    """
    league_table = LeagueTable.objects.get(id=league_table.id, matchday=lea)
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


def get_cup_tables_current_matchday():
    """
    Get queryset of cup tables of the current matchday.
    :return: Queryset of CupTable
    """
    # TODO Measure speed difference
    from django.db.models import Max, Q
    current_matchday_cup_tables = CupTable.objects.values('league_caption').annotate(current_matchday=Max('matchday'))
    q_statement = Q()
    for current_matchday_cup_table in current_matchday_cup_tables:
        q_statement |= (
            Q(league_caption=current_matchday_cup_table['league_caption']) &
            Q(matchday=current_matchday_cup_table['current_matchday'])
        )
    return CupTable.objects.filter(q_statement)
    # return CupTable.objects.raw('''
    #         SELECT cup_table1.id, cup_table1.league_caption, cup_table1.matchday
    #         FROM table_cuptable cup_table1, (
    #           SELECT league_caption, MAX(matchday) AS current_matchday
    #           FROM table_cuptable
    #           GROUP BY league_caption
    #         ) AS cup_table2
    #         WHERE cup_table1.league_caption = cup_table2.league_caption
    #         AND cup_table1.matchday = cup_table2.current_matchday
    #         ''')


def get_league_tables_current_matchday():
    """
    Get queryset of league tables of the current matchday.
    :return: Queryset of LeagueTable
    """
    # TODO Measure speed difference
    from django.db.models import Max, Q
    current_matchday_league_tables = \
        LeagueTable.objects.values('league_caption').annotate(current_matchday=Max('matchday'))
    q_statement = Q()
    for current_matchday_league_table in current_matchday_league_tables:
        q_statement |= (
            Q(league_caption=current_matchday_league_table['league_caption']) &
            Q(matchday=current_matchday_league_table['current_matchday'])
        )
    return LeagueTable.objects.filter(q_statement)
    # return LeagueTable.objects.raw('''
    #         SELECT league_table1.id, league_table1.league_caption, league_table1.matchday
    #         FROM table_leaguetable league_table1, (
    #           SELECT league_caption, MAX(matchday) AS current_matchday
    #           FROM table_leaguetable
    #           GROUP BY league_caption
    #         ) AS league_table2
    #         WHERE league_table1.league_caption = league_table2.league_caption
    #         AND league_table1.matchday = league_table2.current_matchday
    #         ''')


def get_group_standing_average_goals(cup_tables_current_matchday):
    """
    Calculate average goals for a group standing (CupTable).
    :param cup_tables_current_matchday: QuerySet of cup tables of the current matchday
    :return: Average goals for all cup tables of the current matchday
    """
    # TODO Fix Calculation
    return sum(groupstanding.goals for groupstanding in
               (group.groupstanding_set.all() for group in
                (cup_table.group_set.all() for cup_table in
                 cup_tables_current_matchday))) / len(list(cup_tables_current_matchday))


def get_standing_average_goals(league_tables_current_matchday):
    """
    Calculate average goals for a standing (LeagueTable).
    :param league_tables_current_matchday: QuerySet of league tables of the current matchday
    :return: Average goals for all league tables of the current matchday
    """
    # TODO Fix Calculation
    return sum(standing.goals for standing in
               (league_table.standing_set.all() for league_table in
                league_tables_current_matchday)) / len(list(league_tables_current_matchday))
