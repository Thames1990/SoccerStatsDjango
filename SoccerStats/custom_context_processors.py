from competition.models import Competition, CompetitionId


def competition_caption_processor(request):
    return {'captions': Competition.objects.all().values_list('caption', flat=True)}


def competition_league_processor(request):
    return {'leagues': [CompetitionId.reverse_lookup(competition).value for competition in
                        Competition.objects.all().values_list('league', flat=True)]}
