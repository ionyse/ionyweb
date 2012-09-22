# -*- coding: utf-8 -*-

from django.conf import settings
from django.template import RequestContext
from django.template.loader import render_to_string

from djangorestframework.response import Response, ErrorResponse
from djangorestframework import status

from ionyweb.website.rendering import HTMLRendering
from ionyweb.administration.views import IsAdminView
from ionyweb.administration.utils import MESSAGES
from models import Link


class LinksOrderView(IsAdminView):

    def get(self, request, relation_id, plugin, action_pk=None):
        
        # Get the html of the form
        content = render_to_string('plugin_links_list/actions/links_edit_order.html',
                                   {'plugin': plugin,
                                    'relation_id': relation_id},
                                   context_instance = RequestContext(request))

        response = Response(status.HTTP_200_OK, {'html': content,})
        return self.render(response)


    def post(self, request, relation_id, plugin, action_pk=None):

        links_html_id = request.POST.getlist('links_id[]')
        
        if links_html_id:
            # New ordering items
            order = 1
            for link_id in map(lambda s: s.split('-')[1], links_html_id):
                try:
                    obj = Link.objects.get(pk=link_id)
                    if obj.plugin == plugin:
                        obj.order = order
                        obj.save()
                        order += 1
                except Link.DoesNotExist:
                    pass
                
            # Rendering new content
            html = request.page.render_page(request).content

            if isinstance(html, HTMLRendering):
                html = html.content

            response = Response(status.HTTP_200_OK, {'msg': MESSAGES.get('items_edit_success', ""),
                                                     'html': html,
                                                     'placeholder_type': placeholder_type,
                                                     'html_id': relation_id})
            return self.render(response)
            
        else:
            raise ErrorResponse(status.HTTP_400_BAD_REQUEST,
                                {'msg': MESSAGES.get('default_error', "")})
