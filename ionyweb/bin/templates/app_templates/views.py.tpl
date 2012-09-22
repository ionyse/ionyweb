# -*- coding: utf-8 -*-

from django.template import RequestContext
from ionyweb.website.rendering.utils import render_view

# from ionyweb.website.rendering.medias import CSSMedia, JSMedia, JSAdminMedia
MEDIAS = (
    # App CSS
    # CSSMedia('page_{{ app_name }}.css'),
    # App JS
    # JSMedia('page_{{ app_name }}.js'),
    # Actions JSAdmin
    # JSAdminMedia('page_{{ app_name }}_actions.js'),
    )

def index_view(request, page_app):
    return render_view('page_{{ app_name }}/index.html',
                       { 'object': page_app },
                       MEDIAS,
                       context_instance=RequestContext(request))
