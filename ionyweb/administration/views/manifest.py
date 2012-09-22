# -*- coding: utf-8 -*-
import os

from djangorestframework.response import Response
from djangorestframework import status

from django.template.loader import render_to_string
from django.template import RequestContext
from django.conf import settings

from ionyweb.administration.views import IsAdminView
from ionyweb.administration.permissions import _400_BAD_REQUEST
from ionyweb.website.rendering import RenderingContext
from ionyweb.loaders.manifest import layouts_info, themes_info
from ionyweb.administration.utils import MESSAGES


class LayoutsListView(IsAdminView):
    """
    Display the available Layouts List
    """
    def get(self, request):
        """
        Return the list of layouts
        """
        layout_section_slug = request.GET.get('layout_section_slug', None)

        if not layout_section_slug:
            raise _400_BAD_REQUEST

        else:
            rendering_context = RenderingContext(request)
            current_layout_slug = rendering_context.get_layout_template_slug(layout_section_slug)
            # current_layout_slug = os.path.basename(current_layout)
            list_layouts = layouts_info()
            html = render_to_string('administration/manifest/layouts-list.html',
                                    {'list_layouts': list_layouts,
                                     'layout_section_slug': layout_section_slug,
                                     'current_layout_slug': current_layout_slug},
                                    context_instance = RequestContext(request))
            response = Response(status.HTTP_200_OK, {"html": html})
            return self.render(response)


class LayoutListView(IsAdminView):
    """
    Manage the layout of a placeholder.
    """

    def get(self, request):
        """
        Change and preview the layout of a placeholder
        """
        layout_section_slug = request.GET.get('layout_section_slug', None)
        layout_template_slug = request.GET.get('layout_template_slug', None)
        plugin_relation_default = request.GET.getlist('plugin_relation_default[]')
        plugin_relation_default_placeholder = request.GET.getlist('plugin_relation_default_placeholder[]')

        if not layout_section_slug:
            raise _400_BAD_REQUEST

        rendering_context = RenderingContext(request)
        html_layout_rendering = rendering_context.get_html_layout(layout_section_slug,
                                                                  template_file_preview=layout_template_slug)
        
        # Make data for refresh default
        plugin_relation_default_data = []
        for i in xrange(len(plugin_relation_default)):
            plugin_relation_default_data.append({
                    'id': plugin_relation_default[i],
                    'layout_slug': plugin_relation_default_placeholder[i].split(settings.HTML_ID_PLACEHOLDER)[0]})
        # Refresh of default layout section
        layout_default_infos_refresh = rendering_context.refresh_default(layout_section_slug,
                                                                         plugin_relation_default_data)
        
        response = Response(status.HTTP_200_OK,
                            {"msg": MESSAGES.get('layout_edit_succes', ""), 
                             'default_to_add': layout_default_infos_refresh['add'],
                             'default_to_delete': layout_default_infos_refresh['delete'],
                             'layout_section_slug': layout_section_slug,
                             'html': html_layout_rendering})
        return self.render(response)


    def post(self, request):
        """
        Change the page layout
        """
        layout_section_slug = request.POST.get('layout_section_slug', None)
        layout_template_slug = request.POST.get('layout_template_slug', None)
        
        if not layout_section_slug and not layout_template_slug:
            raise _400_BAD_REQUEST
        
        
        rendering_context = RenderingContext(request)
        rendering_context.set_layout_template_file(layout_section_slug, layout_template_slug)

        response = Response(status.HTTP_200_OK,
                            {"msg": MESSAGES.get('layout_edit_succes', "")})
        return self.render(response)


class ThemesListView(IsAdminView):
    """
    Management of the authentication of users.
    """

    def get(self, request):
        """
        Managements of the Themes List
        """

        list_themes = sorted(themes_info(), key=lambda theme: theme['title'].lower())

        html = render_to_string('administration/manifest/themes-list.html',
                                {'list_themes': list_themes,
                                 'current': request.website.theme},
                                context_instance = RequestContext(request))
        
        response = Response(status.HTTP_200_OK, {"html": html})

        return self.render(response)


    def post(self, request):
        """
        Change the page layout
        """
        
        request.website.theme = request.POST['theme_slug']
        request.website.save()

        response = Response(status.HTTP_200_OK,
                            {"msg": MESSAGES.get('layout_edit_succes', "")})

        return self.render(response)
