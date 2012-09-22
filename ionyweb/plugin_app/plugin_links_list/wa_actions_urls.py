# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from ionyweb.administration.actions.utils import get_actions_urls

from models import Link
from forms import LinkForm

# Generic Action View
urlpatterns = get_actions_urls(Link,
                               form_class=LinkForm,
                               sortable=True)
