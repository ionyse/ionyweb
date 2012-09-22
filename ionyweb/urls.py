# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView, RedirectView
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
		       (r'^_jsi18n/$', 'django.views.i18n.javascript_catalog'),
		       url(r'^_admin/doc/', include('django.contrib.admindocs.urls')),
		       url(r'^_admin/', include(admin.site.urls)),
		       url(r'^_grappelli/', include('grappelli.urls')),
		       url(r'^_install/', include('ionyweb.start_website.urls')),
		       url(r'^_tinymce/', include('tinymce.urls')),
		       url(r'^sitemap\.xml$', 'ionyweb.website.views.sitemap'),
		       url(r'^sitemap-(?P<section>.+)\.xml$', 'ionyweb.website.views.sitemap'),

		       # FIXME: SSL_REQUIRED
		       url(r'^_login/', 
                           'ionyweb.authentication.views.crossdomain_login', 
                           name="crossdomain-login"),
                       url(r'^_login.js$', 'ionyweb.authentication.views.auto_auth_js'),

		       # WE ASSURE THAT ORIGINAL DJANGO SITEMAPS VIEWS
		       # CAN BE REVERSED... BUT THEY ARE NEVER CALLED !
		       url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.index',
			   {'sitemaps': {}}),
		       url(r'^sitemap-(?P<section>.+)\.xml$', 'django.contrib.sitemaps.views.sitemap',
			   {'sitemaps': {}}),
		       # ------
		       
		       )

if settings.DEBUG:
	urlpatterns += patterns('',
            url(r'^_medias/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
	    url(r'^_static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),)
