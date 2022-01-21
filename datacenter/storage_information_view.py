from django.utils.timezone import localtime
from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render
from .passcard_info_view import get_duration, format_duration, is_visit_long


def storage_information_view(request):
    indoor_visits = Visit.objects.filter(leaved_at=None)
    non_closed_visits = []

    for visit in indoor_visits:
        is_strange = is_visit_long(get_duration(visit))
        non_closed_visits.append(
            {
                'who_entered': visit.passcard,
                'entered_at': visit.entered_at,
                'duration': format_duration(get_duration(visit), visit),
                'is_strange': is_strange
            }
        )
    context = {
        'non_closed_visits': non_closed_visits,  # не закрытые посещения
    }
    return render(request, 'storage_information.html', context)
