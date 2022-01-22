import datetime
from django.utils.timezone import localtime
from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render


def get_duration(visit):
    enter_time = localtime(visit.entered_at)
    leaving_time = visit.leaved_at
    if leaving_time is None:
        now = localtime(timezone=None)
        time_in = now - enter_time
    else:
        time_in = leaving_time - enter_time
    return time_in


def format_duration(duration, visit):
    if visit.leaved_at is None:
        crutch = -7
        return str(duration)[:crutch]
    else:
        return str(duration)


def is_visit_long(duration):
    condition = datetime.timedelta(hours=1)
    if duration >= condition:
        return True
    else:
        return False


def passcard_info_view(request, passcode):
    passcard = Passcard.objects.get(passcode=passcode)
    this_passcard_visits = []

    visits = Visit.objects.filter(passcard=passcard)
    for visit in visits:
        duration = format_duration(get_duration(visit), visit)
        is_strange = is_visit_long(get_duration(visit))
        this_passcard_visits.append(
            {
                'entered_at': visit.entered_at,
                'duration': duration,
                'is_strange': is_strange
            }
        )


    context = {
        'passcard': passcard,
        'this_passcard_visits': this_passcard_visits
    }
    return render(request, 'passcard_info.html', context)
