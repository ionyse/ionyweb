# -*- coding: utf-8 -*-
from ionyweb.website.rendering.utils import render_view

def index_view(request, plugin):
    
    return render_view(
        plugin.get_templates('plugin_maps/index.html'),
        {'object': plugin})
