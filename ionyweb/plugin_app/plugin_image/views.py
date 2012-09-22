# -*- coding: utf-8 -*-
from django.conf import settings
from ionyweb.website.rendering.utils import render_view
from ionyweb.website.rendering.medias import CSSMedia, JSMedia

RENDER_MEDIAS = (
    # Plugin CSS
    CSSMedia('plugin_image.css'),
    )
LIGHTBOX_MEDIAS = (
    # Lightbox CSS
    CSSMedia('fancybox/jquery.fancybox.css', prefix_file='js'),
    # Lightbox JS
    JSMedia('fancybox/jquery.fancybox.js'),
    JSMedia('ionyweb.lightbox.js'),
    )

def index_view(request, plugin):
    
    if plugin.lightbox:
        MEDIAS = RENDER_MEDIAS + LIGHTBOX_MEDIAS
    else:
        MEDIAS = RENDER_MEDIAS

    return render_view(
        plugin.get_templates('plugin_image/index.html'),
        {'plugin': plugin,
         'image': plugin.image},
        MEDIAS)
