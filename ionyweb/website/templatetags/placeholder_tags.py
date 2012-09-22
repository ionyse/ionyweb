# -*- coding: utf-8 -*-
"""Tags used by ionyweb for placeholders rendering"""

from django import template
from django.conf import settings
from django.template.loader import render_to_string

register = template.Library()


# --------------------------
# Rendering Placeholder Tags
# --------------------------
@register.tag(name="render_placeholder")
def do_render_placeholder(parser, token):
    try:
        tag_name, id_placeholder = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires a single argument" % token.contents.split()[0])

    if not (id_placeholder[0] == id_placeholder[-1] and id_placeholder[0] in ('"', "'")):
        raise template.TemplateSyntaxError(
            "%r tag's argument should be in quotes" % tag_name)
    return PlaceholderNode(id_placeholder[1:-1])


class PlaceholderNode(template.Node):

    def __init__(self, id_placeholder):
        self.id_placeholder = id_placeholder

    def render(self, context):
        layout_section_slug = context.get('layout_slug', None)
        rendering_context = context.get('rendering_context', None)

        if layout_section_slug and rendering_context:
            return rendering_context.get_html_placeholder(layout_section_slug,
                                                          self.id_placeholder,
                                                          context)
        return ''
