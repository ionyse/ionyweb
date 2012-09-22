# -*- coding: utf-8 -*-
from django.conf import settings
from ionyweb.website.rendering.utils import render_view

def index_view(request, plugin):
    
    separator = plugin.get_separator()
    links = plugin.links_enabled

    pages = []
    # Ancestors
    if plugin.ancestors_displayed:
        pages = list(request.page.get_ancestors())

    breadcrumb_items = []
    for page in pages:
        if links:
            item_str = u'<a href="%s">%s</a>' % (page.get_absolute_url(), page.title)
        else:
            item_str = page.title
        breadcrumb_items.append(item_str)
    # Add current page
    breadcrumb_items.append(request.page.title)

    if hasattr(request, settings.BREADCRUMB_OBJECT_TITLE):
        breadcrumb_items.append(getattr(request, settings.BREADCRUMB_OBJECT_TITLE))

    return render_view(plugin.get_templates('plugin_breadcrumb/index.html'),
                       {'object': plugin,
                        'items': breadcrumb_items,
                        'separator': separator})
