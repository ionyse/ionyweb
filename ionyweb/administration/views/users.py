# -*- coding: utf-8 -*-

from ionyweb.administration.views import IsAdminView
from djangorestframework.response import Response, ErrorResponse
from djangorestframework import status
from ionyweb.administration.utils import MESSAGES
from ionyweb.authentication.forms import EditCurrentUser
from django.template.loader import render_to_string
from django.template import RequestContext
from django.contrib.auth.forms import PasswordChangeForm

#
class CurrentUser(IsAdminView):
    
    def get(self, request):
        userform = EditCurrentUser(request.user)
        passform = PasswordChangeForm(request.user)
        html = render_to_string('administration/users/current-user.html',
                                {'userform': userform,
                                 'passform': passform,},
                                context_instance = RequestContext(request))
        
        response = Response(status.HTTP_200_OK, {"html": html})
        return self.render(response)
    
    def post(self, request):

        if 'old_password' in request.POST and request.POST['old_password'] == "":
            userform = EditCurrentUser(request.user, request.POST)
            
            if userform.is_valid():
                userform.save(request.user)
                response = Response(status.HTTP_200_OK, {})
                return self.render(response)
            else:
                passform = PasswordChangeForm(request.user)
                html = render_to_string('administration/users/current-user.html',
                                    {'userform': userform,
                                     'passform': passform,},
                                    context_instance = RequestContext(request))
                
                response = Response(status.HTTP_400_BAD_REQUEST, {"html": html})
                return self.render(response)
            
        else:
            userform = EditCurrentUser(request.user, request.POST)
            passform = PasswordChangeForm(request.user, data=request.POST)
            
            
            if userform.is_valid() and passform.is_valid():
                userform.save(request.user)
                passform.save(request.user)
                
                response = Response(status.HTTP_200_OK, {})
                return self.render(response)
            else:
                
                html = render_to_string('administration/users/current-user.html',
                                {'userform': userform,
                                 'passform': passform,},
                                context_instance = RequestContext(request))
                response = Response(status.HTTP_400_BAD_REQUEST, {"html": html})
                return self.render(response)
            
        raise ErrorResponse(status.HTTP_400_BAD_REQUEST,
                                {'msg': MESSAGES.get('default_error', "")})
