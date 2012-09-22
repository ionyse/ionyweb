# -*- coding: utf-8 -*-
from django.conf import settings
from ionyweb.website.rendering.utils import render_view
from ionyweb.website.rendering.medias import JSAdminMedia

RENDER_MEDIAS = (
    JSAdminMedia('plugin_blog_entries_list.js'),
    )

def index_view(request, plugin):
    
    return render_view(
        plugin.get_templates('plugin_blog_entries_list/index.html'),
        {'object': plugin},
        RENDER_MEDIAS,
        is_admin_view=request.is_admin)
