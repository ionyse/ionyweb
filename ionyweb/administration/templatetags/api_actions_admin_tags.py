# -*- coding: utf-8 -*-

import re

from django.conf import settings
from django.utils.safestring import mark_safe
from django.template import Library

register = Library()

@register.simple_tag
def boolean_icon(field_val):
    BOOLEAN_MAPPING = {True: 'yes', False: 'no', None: 'unknown'}
    return mark_safe(u'<img src="%simg/admin/icon-%s.gif" alt="%s" />' % (settings.ADMIN_MEDIA_PREFIX, BOOLEAN_MAPPING[field_val], field_val))

@register.simple_tag
def url_clean(path):
    """ Remove everything before the wa
    """
    return path[path.find('/'+settings.URL_ADMIN_SEP):]

@register.simple_tag
def url_add(path, pk=None):
    """ Take the path of the object list and generate the wa_url to
    add or edit

    >>> url_add('/foo/bar/wa/action/app-content-1/category_list/')
    '/wa/action/app-content-1/category/'

    >>> url_add('/foo/bar/wa/action/app-content-1/category/2/')
    '/wa/action/app-content-1/category/2/'
    """
    path = url_clean(path).replace(settings.ACTION_ADMIN_LIST_SUFFIX, '')

    if pk is not None:
        path += '%s/' % pk

    return path

@register.simple_tag
def url_list(path):
    """ Take the path of the object edition or creation form and
    generate the wa_url of the list

    >>> url_list('/foo/bar/wa/action/app-content-1/category/2/')
    '/wa/action/app-content-1/category_list/'

    """
    match = re.match(r'^.*(/wa/[A-Za-z0-9/-]+)([A-Za-z-]+)/([0-9]+/)?$', path)
    return u'%s%s%s/' % (match.group(1), match.group(2), 
                         settings.ACTION_ADMIN_LIST_SUFFIX)

@register.simple_tag
def url_order(path):
    path = url_clean(path).replace(settings.ACTION_ADMIN_LIST_SUFFIX, 
                                   settings.ACTION_ADMIN_ORDER_SLUG)
    return path

@register.simple_tag(takes_context=True)
def render_result_action_list(context, obj):
    result = ""
    for attr in context['list_display']:
        attr_obj = getattr(obj, attr)
        if callable(attr_obj):
            render_attr = u'%s' % attr_obj()
        else:
            render_attr = u'%s' % attr_obj
        result += "<td>%s</td>" % render_attr
    return result

