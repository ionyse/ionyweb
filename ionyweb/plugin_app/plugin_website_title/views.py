# -*- coding: utf-8 -*-
from ionyweb.website.rendering.utils import render_view
from ionyweb.website.rendering.medias import CSSMedia

RENDER_MEDIAS = (
    # Plugin CSS
    CSSMedia('plugin_website_title.css'),
    )

def index_view(request, plugin):

    if plugin.link_enabled:
        medias = RENDER_MEDIAS
    else:
        medias = None

    return render_view(
        plugin.get_templates('plugin_websitetitle/index.html'),
        {'default_title': request.website.title,
         'object': plugin}, medias)
