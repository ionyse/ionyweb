# -*- coding: utf-8 -*-
from django import template
from ionyweb.administration.actions.utils import get_actions_for_object_model

register = template.Library()


@register.tag(name="actions_admin")
def do_actions_admin(parser, token):
    try:
        tag_name, obj = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires a single argument" % token.contents.split()[0])
    return ActionsAdminNode(obj)


class ActionsAdminNode(template.Node):
    def __init__(self, obj, *args, **kwargs):
        super(ActionsAdminNode, self).__init__(*args, **kwargs)
        self.obj = template.Variable(obj)

    def render(self, context):
        # We render only if admin viewing
        if context.get('is_admin', None):
            try:
                # Get the object model into context
                obj = self.obj.resolve(context)
                actions_obj = get_actions_for_object_model(obj)
                if actions_obj['list']:
                    return u'<div class="wa_actions_object_widget"><p>%s : %s</p></div>' % ( actions_obj['title'], u' -'.join(actions_obj['list']))
            except template.VariableDoesNotExist:
                pass
        return u''
