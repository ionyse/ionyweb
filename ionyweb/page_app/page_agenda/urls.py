# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from views import index_view

urlpatterns = patterns('',
                       url(r'^$', index_view),
                       url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/$', index_view),
                       url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$', index_view),
                       )
