# -*- coding: utf-8 -*-

from ionyweb.administration.actions.utils import get_actions_urls
from models import Event
from forms import EventForm

urlpatterns = get_actions_urls(Event,
                               form_class=EventForm,
                               list_display=('title', 
                                             'display_description_admin', 
                                             'start_date', 
                                             'is_published', 
                                             'last_modif'))
