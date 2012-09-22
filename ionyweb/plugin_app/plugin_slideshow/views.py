# -*- coding: utf-8 -*-
from django.conf import settings
from ionyweb.website.rendering.medias import *
from ionyweb.website.rendering.utils import render_view

RENDER_MEDIAS = (
    JSMedia('ionyweb.timer.js'),
    JSMedia('ionyweb.slideshow.js'),
    CSSMedia('plugin_slideshow.css'),
    JSAdminMedia('plugin_slideshow_actions.js')
    )


def index_view(request, plugin):
    
    return render_view(
        plugin.get_templates('plugin_slideshow/index.html'),
        {'object': plugin,
         'slides_list': plugin.slides_list},
        RENDER_MEDIAS, is_admin_view=request.is_admin)
