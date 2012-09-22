# -*- coding: utf-8 -*-
from django.template.loader import render_to_string
from ionyweb.website.rendering import HTMLRendering


def render_view(template_name, params={}, medias=(), context_instance=None, is_admin_view=False, title=None):
    """
    Returns an HTMLRendering object.

    Shortcut used by all IonyWeb apps or plugins.
    """
    content = render_to_string(template_name,
                               params,
                               context_instance)
    try:
        admin_view = context_instance['is_admin']
    except TypeError, KeyError:
        admin_view = is_admin_view

    if admin_view:
        # All medias are used
        rendering_medias = medias
    else:
        # AdminMedias are not used
        rendering_medias = tuple([media for media in medias if not media.admin])
    return HTMLRendering(content, rendering_medias, title=title)
