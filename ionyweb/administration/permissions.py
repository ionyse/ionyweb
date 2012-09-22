# -*- coding: utf-8 -*-
from djangorestframework.permissions import BasePermission

from djangorestframework import status
from djangorestframework.response import ErrorResponse

_400_BAD_REQUEST = ErrorResponse(
    status.HTTP_400_BAD_REQUEST,
    {'detail': 'Bad request'})

_403_FORBIDDEN_RESPONSE = ErrorResponse(
    status.HTTP_403_FORBIDDEN,
    {'detail': 'You do not have permission to access this resource. ' +
               'You may need to login or otherwise authenticate the request.'})

class IsAdminUser(BasePermission):
    """
    Allows access only to admin users.
    """

    def check_permission(self, user):
        # Thow possibilities
        # 1. is_staff
        # 2. is_website_owner
        if not user.is_staff and user not in self.view.request.website.owners.all():
            raise _403_FORBIDDEN_RESPONSE

class IsSuperAdminUser(BasePermission):
    """
    Allows access only to admin users.
    """

    def check_permission(self, user):
        # Thow possibilities
        # 1. is_staff
        # 2. is_website_owner.is_superuser
        if (not user.is_staff and 
            user not in self.view.request.website.owners.filter(websites_owned__is_superuser=True)):
            raise _403_FORBIDDEN_RESPONSE
