# -*- coding: utf-8 -*-
"""
URLs of ``blog`` application.
"""
from django.conf.urls import patterns, url

import django.views.generic
import django.views.generic.list_detail
from views import entries_queryset_view_to_app, categories_queryset_view_to_app
from feeds import RssEntries, RssCategory

urlpatterns = patterns('',
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[\w-]+)/$',
        entries_queryset_view_to_app(django.views.generic.date_based.object_detail),
        dict(
            month_format='%m',
            date_field='publication_date',
            slug_field='slug',
        ),
        name='blog_entry',
    ),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$',
        entries_queryset_view_to_app(django.views.generic.date_based.archive_day),
        dict(
            month_format='%m',
            date_field='publication_date',
        ),
        name='blog_day',
    ),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/$',
        entries_queryset_view_to_app(django.views.generic.date_based.archive_month),
        dict(
            month_format='%m',
            date_field='publication_date',
        ),
        name='blog_month',
    ),
    url(r'^(?P<year>\d{4})/$',
        entries_queryset_view_to_app(django.views.generic.date_based.archive_year),
        dict(
            make_object_list=True,
            date_field='publication_date',
        ),
        name='blog_year',
    ),
    url(r'^(?P<slug>[\w-]+)/$',
        categories_queryset_view_to_app(django.views.generic.list_detail.object_detail),
        dict(
            slug_field='slug'
        ),
        name='blog_category',
    ),
    url(r'^$',
        entries_queryset_view_to_app(django.views.generic.date_based.archive_index),
        dict(
            date_field='publication_date',
        ),
        name='blog',
    ),

    url(r'^feed/rss/$', RssEntries(), name='blog_rss_entries_feed'),
    url(r'^feed/rss/(?P<slug>[\w-]+)/$', RssCategory(), name='blog_rss_category_feed'),
)
