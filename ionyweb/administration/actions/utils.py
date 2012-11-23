# -*- coding: utf-8 -*-
from django.utils.translation import ugettext as _
from django.conf.urls import patterns, url

from ionyweb.page.models import AbstractPageApp
from ionyweb.plugin.models import AbstractPlugin


def get_actions_urls(model, url_name=None, **kwargs):
    """
    Get automatically the actions urls for a model.

    """
    from ionyweb.administration.actions.views import (ActionAdminListView,
                                                      ActionAdminDetailView,
                                                      ActionAdminOrderView)

    app_label = model._meta.app_label
    # Url Name
    if url_name is None:
        module_name = model._meta.module_name
    else:
        module_name = url_name

    # Specific Detail View
    try:
        DetailView = kwargs.pop('detail_view_class')
    except KeyError:
        DetailView = ActionAdminDetailView
    # Specific List View
    try:
        ListView = kwargs.pop('list_view_class')
    except KeyError:
        ListView = ActionAdminListView
    # Prefix URL
    try:
        prefix_url = kwargs.pop('prefix_url')
    except KeyError:
        prefix_url = ''

    # Args Management
    def filter_kwargs(exclude_args, kwargs):
        new_kwargs = kwargs.copy()
        for arg in exclude_args:
            if arg in new_kwargs:
                del new_kwargs[arg]
        return new_kwargs

    list_kwargs = filter_kwargs(['form_class'], kwargs)
    detail_kwargs = filter_kwargs(['ordering', 'sortable', 'sortable_field', 'list_display'], kwargs)

    urlpatterns = patterns('',
                           # Change List Action
                           url(r'^%s%s_list/$' % (prefix_url, module_name),
                               ListView.as_view(model=model, **list_kwargs),
                               name='wa-%s-%s_list-action' % (app_label, module_name)),
                           
                           # Object Detail Action
                           url(r'^%s%s/(?P<object_pk>[0-9]*)/$' % (prefix_url, module_name),
                               DetailView.as_view(model=model, **detail_kwargs),
                               name='wa-%s-%s-action' % (app_label, module_name)),

                           # Object Creation Action
                           url(r'^%s%s/$' % (prefix_url, module_name),
                               DetailView.as_view(model=model, **detail_kwargs),
                               name='wa-%s-%s-creation-action' % (app_label, module_name)),
                           )
    if kwargs.get('sortable', False):
        urlpatterns += patterns('',
                                url(r'^%s%s_order/$' % (prefix_url, module_name),
                                    ActionAdminOrderView.as_view(model=model),
                                    name='wa-%s-%s_order-action' % (app_label, module_name)),
                                )
    return urlpatterns


def get_actions_for_object_model(obj, relation_id=None):

    # -- DEPRECATED --
    # Only for backward compatibilty
    if hasattr(obj, 'get_actions'):
        # All app and plugin define a get_actions method,
        # so we check if the method is overloaded...
        get_actions = getattr(obj, 'get_actions')
        if get_actions():
            # Actions
            actions_html = []
            for action in get_actions():
                actions_html.append(u'<a onclick="%s(\'%s\'); return false;">%s</a>' % (
                        action[1],
                        relation_id,
                        action[0]))
            # Title
            title = obj.__class__.get_name()
            # Relation ID
            if not relation_id:
                relation_id = obj.get_relation_id()
            return {'title': title, 'list': actions_html}
    # -- NEW SYNTAX --
    # Only if object model defines ActionsAdmin inner class.
    if hasattr(obj, 'ActionsAdmin'):
        # Get title of actions group (or default value)
        title = getattr(obj.ActionsAdmin, 'title', _(u'Actions'))
        # Get relation_id for the first param of WA urls
        if not relation_id:
            related_obj = obj
            if not isinstance(obj, AbstractPageApp) and not isinstance(obj, AbstractPlugin):
                related_object_path = getattr(obj.ActionsAdmin, 'related_object', 'app')
                for item in related_object_path.split('__'):
                    related_obj = getattr(related_obj, item)
            relation_id = related_obj.get_relation_id()
        # Make actions list
        actions_html = []
        for action in getattr(obj.ActionsAdmin, 'actions_list', []):
            # Formating each argument (in string)
            # in order to provide the callback function
            args_formated = u''
            for arg in action.get('args', []):
                try:
                    args_formated += u', %s' % getattr(obj, arg)
                except AttributeError:
                    pass
            actions_html.append(
                u'<a onclick="%s(\'%s\'%s); return false;">%s</a>' % (
                    action.get('callback'),
                    relation_id,
                    args_formated,
                    action.get('title'))
                )
        return {'title': title, 'list': actions_html}
    return {}
