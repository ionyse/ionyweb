# -*- coding: utf-8 -*-
from django.template import RequestContext
from ionyweb.website.rendering.utils import render_view

# from ionyweb.rendering.medias import CSSMedia, JSMedia, JSAdminMedia
MEDIAS = (
    # App CSS
    # CSSMedia('page_{{ plugin_name }}.css'),
    # App JS
    # JSMedia('page_{{ plugin_name }}.js'),
    # Actions JSAdmin
    # JSAdminMedia('page_{{ plugin_name }}_actions.js'),
    )

def index_view(request, plugin):    
    return render_view('plugin_{{ plugin_name }}/index.html',
                       {'object': plugin},
                       MEDIAS,
                       context_instance=RequestContext(request))
