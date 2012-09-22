# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from ionyweb.administration.actions.utils import get_actions_urls

from models import EntryLink
from forms import EntryLink_Form

# Generic Action View
urlpatterns = get_actions_urls(EntryLink,
                               form_class=EntryLink_Form,
                               sortable=True)
