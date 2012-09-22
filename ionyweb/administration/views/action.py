# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.urlresolvers import resolve
from django.http import Http404

from djangorestframework.response import ErrorResponse
from djangorestframework import status

from ionyweb.plugin.models import PluginRelation
from ionyweb.administration.views import IsAdminView
from ionyweb.administration.utils import MESSAGES, check_object_html_id


class ActionView(IsAdminView):
    """
    Views dispatcher for actions of objects.
    """

    def base_view(self, request, html_id_object, url_action):
        """
        Basic View of actions admin.

        This method gets the object related to the request
        and return the action asked.
        """
        # Get and check app/plugin object HTML ID
        # Types accepted : PluginRelation or App
        # If slug not valid => raise HTTP_400_BAD_REQUEST
        object_type, object_id = check_object_html_id(
            html_id_object, types=[settings.SLUG_PLUGIN, settings.SLUG_APP])

        # Case #1 - Object Type : PluginRelation
        if object_type == settings.SLUG_PLUGIN:
            # Get plugin relation
            try:
                obj_relation = PluginRelation.objects\
                    .get(id__exact=object_id)
            except PluginRelation.DoesNotExist:
                # If the plugin is not found => 404
                raise ErrorResponse(status.HTTP_404_NOT_FOUND,
                                    {'msg': MESSAGES.get('default_error', "")})
            # Get plugin object
            obj = obj_relation.content_object

        # Case #2 - Object Type : App
        # Necessarily : object_type == settings.SLUG_APP:
        else:
            # Get app object
            obj = request.page.app_page_object
            # We check that slug parameter is correct
            if obj.pk != int(object_id):
                raise ErrorResponse(status.HTTP_404_NOT_FOUND,
                                    {'msg': MESSAGES.get('default_error', "")})

        # Formatting url action
        # (add '/' at the begining and the ending)
        if url_action[0] != '/': 
            url_action = '/' + url_action
        if url_action[-1] != '/': 
            url_action = url_action + '/'

        # Dispatcher View
        try:
            match = resolve(url_action, urlconf=obj.get_actions_urlconf())
            return match.func(request, html_id_object, obj, **match.kwargs)
        except Http404:
            raise ErrorResponse(status.HTTP_404_NOT_FOUND,
                                {'msg': MESSAGES.get('action_not_found', "")})
        

    def get(self, *args, **kwargs):
        return self.base_view(*args, **kwargs)

    def put(self, *args, **kwargs):
        return self.base_view(*args, **kwargs)

    def post(self, *args, **kwargs):
        return self.base_view(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        return self.base_view(*args, **kwargs)
