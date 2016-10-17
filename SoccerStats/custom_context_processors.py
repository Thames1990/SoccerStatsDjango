from competition.util import fetch_cup_ids, fetch_league_ids, fetch_cup_names, fetch_league_names


def cup_id_processor(request):
    return {'cup_ids': fetch_cup_ids()}


def cup_name_processor(request):
    return {'cup_names': fetch_cup_names()}


def league_id_processor(request):
    return {'league_ids': fetch_league_ids()}


def cup_league_processor(request):
    return {'league_names': fetch_league_names()}
