from competition.models import CupID, LeagueID


def cup_id_processor(request):
    return {
        'cup_ids': [cup_id for cup_id in CupID]
    }


def league_id_processor(request):
    return {
        'league_ids': [league_id for league_id in LeagueID]
    }
