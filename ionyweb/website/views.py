# -*- coding: utf-8 -*-
import os.path

from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse, resolve
from django.db import transaction, connection
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, Http404
from django.shortcuts import get_object_or_404, render_to_response
from django.views.generic import UpdateView, FormView, ListView, DeleteView
from django.views.generic.detail import SingleObjectMixin
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.template import RequestContext
from django.template.loader import render_to_string
from django.contrib.sitemaps.views import (sitemap as django_sitemap,
                                           index as django_index)

from ionyweb.utils import get_sitemaps
from ionyweb.website.decorators import website_superuser
from ionyweb.website.models import WebSiteOwner, WebSite
from ionyweb.website.utils import get_sha1_params_url, main_menus
from ionyweb.website.rendering import HTMLRendering, RenderingContext
from ionyweb.page.models import Page
from ionyweb.plugin.models import PluginRelation


# Render Site pages
def render_website(request, path_info, render_content_only=False):
    'Important view that display the requested path of the requested site'

    # Get the infos of page to display
    page_infos = get_sha1_params_url(path_info)
    # Urls not valid
    if page_infos['error']:
        return None
    # Save the app url for url dispatcher
    request.url_app = page_infos['params']
    # ----------------------
    # Get concerned page
    # --
    try:
        request.page = request.website.pages.select_related().get(sha1=page_infos['sha1'])
    except Page.DoesNotExist:
        return None
    # ----------------------
    # WebSite admin Url
    # --
    if page_infos['admin']:
        request.is_admin_url = True
        try:
            # Loading admin website views
            match = resolve(page_infos['params_admin'], urlconf=settings.URLCONF_WEBSITE_ADMIN)
            return match.func(request, **match.kwargs)
        except Exception:
            raise
    else:
        request.is_admin_url = False
    # ----------------------
    # WebSite Page rendering
    # --
    if request.page:

        if request.website.in_maintenance and not request.is_admin:
            templates = [os.path.join('themes', request.website.theme, settings.TEMPLATE_MAINTENANCE_DEFAULT),
                         os.path.join('themes', settings.TEMPLATE_MAINTENANCE_DEFAULT)]
            response = render_to_response(templates,
                                          context_instance=RequestContext(request))
            response.status_code = 503
            return response

        # If page is a draft, 404 for visitor and display for administrator
        if request.page.draft and not request.is_admin:
            raise Http404
        
        # Rendering Context of Modulo3
        rendering_context = RenderingContext(request)
        # rendering_context.debug()
        
        # Maybe App sent redirection or http response.
        if rendering_context.http_response:
            return rendering_context.http_response

        if render_content_only:
            return render_to_string(rendering_context.theme_templates,
                                    {'rendering_context': rendering_context},
                                    context_instance=RequestContext(request))
        else:
            return render_to_response(rendering_context.theme_templates,
                                      {'rendering_context': rendering_context},
                                      context_instance=RequestContext(request))



def sitemap(request, section=None):
    sitemaps = get_sitemaps()
    if settings.SITEMAP_INDEX and not section:
        return django_index(request, sitemaps)
    else:
        return django_sitemap(request, sitemaps, section=section)
