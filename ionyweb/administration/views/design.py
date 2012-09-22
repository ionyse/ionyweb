# -*- coding: utf-8 -*-

from django.conf import settings
from ionyweb.administration.views import IsSuperAdminView
from djangorestframework.response import Response
from djangorestframework import status
from ionyweb.administration.utils import MESSAGES

from django.template.loader import render_to_string
from django.template import RequestContext

from ionyweb.loaders.manifest import themes_info

from ionyweb.design.views import get_list_design

class DesignList(IsSuperAdminView):
    
    def get(self, request):
        
        list_themes = sorted(get_list_design(request), key=lambda theme: theme['title'].lower())

        if not request.user.is_staff:
            list_themes = [ti for ti in list_themes if ti['slug'] not in settings.RESTRICTED_THEMES]

        # Render HTML
        html = render_to_string('administration/design/themes_list.html',
                                {'list_themes': list_themes,
                                 'current': request.website.theme},
                                context_instance = RequestContext(request))
        
        response = Response(status.HTTP_200_OK, {"html": html})
        return self.render(response)
    
    

#
class DesignStylesList(IsSuperAdminView):
    
    def get(self, request, pk=None):
        
       
        current_theme = request.website.theme.split('/')[0]
        try:
            current_style = request.website.theme.split('/')[1]
        except:
            current_style = None
        # Render HTML
        
        if not pk:
            pk = current_theme
        theme = themes_info(pk)[0]
        
        html = render_to_string('administration/design/styles_list.html',
                                {'theme': theme,
                                 'current_theme': current_theme,
                                 'current_style': current_style},
                                context_instance = RequestContext(request))
        
        response = Response(status.HTTP_200_OK, {"html": html, 'current': current_theme})
        return self.render(response)
    
    def post(self, request, pk=None):
        """
        Change the page Theme
        """
        request.website.theme = request.POST['theme_slug']
        request.website.save()

        response = Response(status.HTTP_200_OK,
                            {"msg": MESSAGES.get('theme_edit_succes', "")})

        return self.render(response)
#
#
class DesignStylesPreview(IsSuperAdminView):
    
    def get(self, request):
        return get_list_design(request)
                
class DesignStylesSave(IsSuperAdminView):
    
    def get(self, request):
        return get_list_design(request)
                