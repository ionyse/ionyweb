# -*- coding: utf-8 -*-
import sys

from django.middleware.csrf import CsrfViewMiddleware
from djangorestframework.authentication import BaseAuthentication
from djangorestframework.views import View
from djangorestframework.permissions import IsAuthenticated
from ionyweb.administration.permissions import IsAdminUser, IsSuperAdminUser
from django.utils.crypto import constant_time_compare

class UserLoggedInAuthentication(BaseAuthentication):
    """
    Use Django's session framework for authentication.
    """

    def authenticate(self, request):
        """
        Returns a :obj:`User` if the request session currently has a logged in user.
        Otherwise returns :const:`None`.
        """
        # TODO: Switch this back to request.POST, and let
        # FormParser/MultiPartParser deal with the consequences.
        if getattr(request, 'user', None) and request.user.is_active:
            # If this is a POST request we enforce CSRF validation.
            # if request.method.upper() in ['POST', 'PUT', 'DELETE']:
            #     DATA = self.view.DATA
            #     print DATA

            #     csrf_token = request.META.get('CSRF_COOKIE')

            #     if csrf_token is not None:
            #         request_csrf_token = DATA.get('csrfmiddlewaretoken', None)

            #         if request_csrf_token is None:
            #             sys.stderr.write('\n\nManque le cookie\n\n')
            #             # Fall back to X-CSRFToken, to make things easier for AJAX
            #             request_csrf_token = request.META.get('HTTP_X_CSRFTOKEN', '')
                        
            #         print request_csrf_token, csrf_token
            #         if constant_time_compare(request_csrf_token, csrf_token):
            #             return request.user
            #     else:
            #         sys.stderr.write('NO CSRF COOKIE')

            #     sys.stderr.write('\n\nCSRF FAILED\n\n')
            #     return None

            return request.user
        return None

class IsLoggedInView(View):
    authentication = (UserLoggedInAuthentication, )
    permissions = (IsAuthenticated, )

class IsAdminView(IsLoggedInView):
    permissions = (IsAuthenticated, IsAdminUser)

class IsSuperAdminView(IsLoggedInView):
    permissions = (IsAuthenticated, IsSuperAdminUser)
