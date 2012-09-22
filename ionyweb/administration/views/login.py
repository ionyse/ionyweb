# -*- coding: utf-8 -*-
from djangorestframework.views import View
from djangorestframework.response import Response
from djangorestframework import status

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from ionyweb.administration.utils import MESSAGES


class LoginView(View):
    """
    Management of the authentication of users.
    """        

    def post(self, request):
        """
        Handle POST requests, managing the user authentication.
        """
        
        try:
            user = User.objects.get(email=request.POST['email'])
            user = authenticate(username=user.username, password=request.POST['password'])
          
            if user is not None:
                if user.is_active:
                    login(request, user)
                    response = Response(status.HTTP_200_OK,
                                        {"msg": MESSAGES.get('user_authenticated', "")})
                else:
                    response = Response(status.HTTP_400_BAD_REQUEST,
                                        {"msg": MESSAGES.get('inactive_user', "")})
                    
            else:
                response = Response(status.HTTP_400_BAD_REQUEST,
                                    {"msg": MESSAGES.get('bad_login_pwd', "")})

        except User.DoesNotExist:            
            response = Response(status.HTTP_400_BAD_REQUEST,
                                {"msg": MESSAGES.get('bad_login_pwd', "")})
            
        return self.render(response)

class LogoutView(View):
    """
    Manager de Logout
    """
    
    def get(self, request):
        logout(request)
        response = Response(status.HTTP_200_OK)

        return self.render(response)
