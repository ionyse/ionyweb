# -*- coding: utf-8 -*-
"""Tags used by ionyweb for template themes rendering"""

from django import template
from django.conf import settings
from django.template.loader import render_to_string
from ionyweb.administration.utils import is_page_placeholder_html_id

register = template.Library()


# ----------------------
# Rendering Content Tags
# ----------------------

# page layout rendering
@register.tag
def render_layout(parser, token):
    try:
        tag_name, layout_slug = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires a single argument" % token.contents.split()[0])
    if not (layout_slug[0] == layout_slug[-1] and layout_slug[0] in ('"', "'")):
        raise template.TemplateSyntaxError("%r tag's argument should be in quotes" % tag_name)
    if is_page_placeholder_html_id(layout_slug[1:-1]):
        raise template.TemplateSyntaxError("%r tag's argument shouldn't start with the value : '%s'" % (
                tag_name, settings.SLUG_CONTENT))
    return RenderLayoutNode(layout_slug[1:-1])

# page rendering
@register.tag
def render_page(parser, token):
    token_items = token.split_contents()
    # The first item is necessarily the tag name
    tag_name = token_items[0]
    layout_name = None
    # One argument (optional) ==> name of layout
    if len(token_items) == 2:
        layout_name = token_items[1]
        if not (layout_name[0] == layout_name[-1] and layout_name[0] in ('"', "'")):
            raise template.TemplateSyntaxError("%r tag's argument should be in quotes" % tag_name)
    # Too much arguments
    elif len(token_items) > 2:
        raise template.TemplateSyntaxError(
            "%r tag accept only one optional argument" % tag_name)
    # Make layout slug rendering
    layout_slug = settings.SLUG_CONTENT
    if layout_name:
        layout_slug += '%s%s' % (settings.SLUG_SEP, layout_name[1:-1])
    return RenderLayoutNode(layout_slug)

class RenderLayoutNode(template.Node):

    def __init__(self, layout_section_slug):
        self.layout_section_slug = layout_section_slug
        
    def render(self, context):
        rendering_context = context.get('rendering_context', None)
        if rendering_context:
            return '<div id="%s">%s</div>' % (u'%s%s' % (settings.HTML_ID_LAYOUT, self.layout_section_slug),
                                              rendering_context.get_html_layout(self.layout_section_slug, context))
        return ''

# page title rendering
@register.simple_tag(takes_context=True)
def title(context):
    rendering_context = context.get('rendering_context', None)
    if rendering_context:
        return rendering_context.page_title

# site name rendering
@register.simple_tag(takes_context=False)
def site_name():
    return settings.SITE_NAME

# page navigation rendering
@register.simple_tag(takes_context=True)
def render_navigation(context):
    rendering_context = context.get('rendering_context', None)
    if rendering_context:
        return '<div id="%s">%s</div>' % (
            settings.HTML_ID_NAV,
            rendering_context.html_navigation)
    return ''

# default placeholder page rendering
@register.simple_tag(takes_context=True)
def render_default(context):
    rendering_context = context.get('rendering_context', None)
    if rendering_context:
        return rendering_context.get_html_placeholder_default(context)
    return ''

# clipboard placeholder page rendering
@register.simple_tag(takes_context=True)
def render_clipboard(context):
    rendering_context = context.get('rendering_context', None)
    if rendering_context:
        return rendering_context.get_html_placeholder_clipboard(context)
    return ''


# ----------------------
# Rendering Medias Tags
# ----------------------

# render_medias
@register.simple_tag(takes_context=True)
def render_medias(context):
    html_medias = '<script type="text/javascript">ionyweb = {};</script>';
    # for media in context.get("medias_page", []):
    #     if media:
    #         html_medias += media
    # return html_medias
    context_rendering = context.get('rendering_context', None)
    if context_rendering:
        html_medias += context_rendering.html_medias
    return html_medias

# ----------------------
# Rendering Metas Tags
# ----------------------

# Keywords
@register.simple_tag(takes_context=True)
def render_meta_kw(context):
    page = context.get('page', None)
    if page:
        kw = page.get_meta_keywords()
        if kw:
            return u'<meta name="keywords" content="%s" />' % kw
    return u''

# Description
@register.simple_tag(takes_context=True)
def render_meta_description(context):
    page = context.get('page', None)
    if page:
        description = page.get_meta_description()
        if description:
            return u'<meta name="description" content="%s" />' % description
    return u''

# Favicon
@register.simple_tag(takes_context=True)
def render_favicon(context, filename='favicon.ico'):
    """
    Return favicon link for current theme.
    
    By default return the file 'favicon.ico' in root theme dir.
    You can override this file with parameter.
    """
    website = context['request'].website
    if website:
        favicon_link = u'<link rel="shortcut icon" type="image/png" href="%sthemes/%s/%s" />' % (
            context.get('STATIC_URL', ''), website.theme, filename)
        return favicon_link
    return u''
                                         


# -----------------------------
# Google Analytics Tags
# -----------------------------

@register.inclusion_tag('page/google_analytics-tracking_code.html', takes_context=True)
def googleanalytics(context, tracking_code=None):
    """
    Includes the google analytics tracking code, using the code number in
    GOOGLE_ANALYTICS_ACCOUNT_CODE setting or the tag's param if given.
    
    Syntax::
    
        {% googleanalytics [code_number] %}
    
    Example::
    
        {% googleanalytics %}

        or if you want to override account code the code:

        {% googleanalytics "UA-000000-0" %}

    """
    if not tracking_code:
        request = context['request']
        if request.website.analytics_key:
            tracking_code = request.website.analytics_key
        else:
            tracking_code = getattr(settings, 'GOOGLE_ANALYTICS_ACCOUNT_CODE', None)
    use_legacy_code = getattr(settings, 'GOOGLE_ANALYTICS_LEGACY_CODE', False)
    return {'tracking_code': tracking_code, 'use_legacy_code': use_legacy_code}


# -----------------------------
# Rendering Administration Tags
# -----------------------------

# admin_toolbar
@register.inclusion_tag('administration/admin_toolbar_tag.html', takes_context=True)
def admin_toolbar(context):
    """
    Returns the administration skeleton of Modulo.
    """
    return context

# admin_toolbar_medias
@register.inclusion_tag('administration/admin_toolbar_medias_tag.html', takes_context=True)
def admin_toolbar_medias(context):
    """
    Returns the administration skeleton of Modulo.
    """
    context['admin_theme'] = settings.ADMIN_THEME
    context['debug'] = settings.DEBUG
    return context


# --------------------------
# Rendering Widget Tags
# --------------------------
class WidgetNode(template.Node):

    def __init__(self, widget_slug):
        self.widget_slug = widget_slug

    def render(self, context):
        try:
            return context['widgets'][self.widget_slug]
        except KeyError:
            context['widget_slug'] = self.widget_slug
            return render_to_string('errors/empty_widget.html', context)

@register.tag(name="render_widget")
def do_render_widget(parser, token):
    try:
        tag_name, widget_slug = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires a single argument" % token.contents.split()[0])

    if not (widget_slug[0] == widget_slug[-1] and widget_slug[0] in ('"', "'")):
        raise template.TemplateSyntaxError(
            "%r tag's argument should be in quotes" % tag_name)
    return WidgetNode(widget_slug[1:-1])
