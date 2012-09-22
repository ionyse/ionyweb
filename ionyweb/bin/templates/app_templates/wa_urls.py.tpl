# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from wa_views import admin_index_view

urlpatterns = patterns('',
                       url(r'^$', admin_index_view),
                       )
