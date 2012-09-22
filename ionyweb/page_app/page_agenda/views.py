# -*- coding: utf-8 -*-

from django.template import RequestContext
from django.http import HttpResponseRedirect

from ionyweb.website.rendering.medias import CSSMedia, JSAdminMedia
from ionyweb.website.rendering.utils import render_view
import datetime

MEDIAS = (
    CSSMedia('page_agenda.css'),
    JSAdminMedia('page_agenda_actions.js'),
    )

def index_view(request, page_app, year=None, month=None, day=None):

    if year is None:
        today = datetime.date.today()
        month = today.month
        year = today.year
        return HttpResponseRedirect('p/%d/%s/' % (year, str(month).zfill(2)))
    else:
        year = int(year)
        month = int(month)

    prev_year = year-1
    next_year = year+1
    
    prev_month = (month-2) % 12 + 1
    next_month = (month) % 12 + 1

    events = page_app.get_events_for_date(year, month, day)
    url = page_app.get_absolute_url()

    return render_view('page_agenda/index.html',
                       {'object': page_app,
                        'events': events,
                        'url': url,
                        'month': month,
                        'year': year,
                        'prev_month': prev_month,
                        'next_month': next_month,
                        'prev_year': prev_year,
                        'next_year': next_year,
                        },
                       MEDIAS,
                       context_instance=RequestContext(request))
