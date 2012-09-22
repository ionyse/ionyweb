# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from ionyweb.start_website.views import index

urlpatterns = patterns(
    '',
    # Temporary redirect
    url('^$', index),
    
    )
