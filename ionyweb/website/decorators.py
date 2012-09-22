# -*- coding: utf-8 -*-
""" Aeris Decorators """

try:
    from functools import wraps
except ImportError:
    from django.utils.functional import wraps  # Python 2.4 fallback.

from django.contrib.auth.decorators import user_passes_test, login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.utils.decorators import available_attrs
from django.utils.translation import ugettext as _

from ionyweb.website.models import WebSiteOwner

admin_required = user_passes_test(lambda u: (u.is_authenticated()
                                             and u.is_superuser))

def forbidden_access():
    ' Returns a 403 error with a forbidden message that only hacker will get '
    return HttpResponseForbidden(_(u"<h1>You cannot modify this website since "
                                   u"you do not own it.</h1>"))

# @decorator('Arguments')
# def fonction():
#     ...
# is equivalent to : decorator('Arguments')(fonction)
# So decorator('Arguments') should return a decorator


#---
# Aeris Dashboard decorators
#---
def website_right(is_superuser):
    ''' Returns a decorator regarding is_superuser '''
    def decorator(view_func):
        ''' Decorator that provide the current_site and verify the
        access_right of the user '''
        @wraps(view_func, assigned=available_attrs(view_func))
        def __wrapped_view(request, website_id, *args, **kwargs):
            queryset = request.user.websites_owned

            if is_superuser is not None:
                queryset = queryset.filter(is_superuser=is_superuser)

            try:
                request.current_site = \
                    queryset.get(website__id=website_id).website
            except WebSiteOwner.DoesNotExist:
                request.current_site = None
                return forbidden_access()

            return view_func(request, website_id, *args, **kwargs)
        return login_required(__wrapped_view)
    return decorator

website_owner =  website_right(is_superuser=None)
website_owner_only = website_right(is_superuser=False)
website_superuser = website_right(is_superuser=True)



#---
# Website Admin Ajax decorators
#---
def ajax_website_right(is_superuser):
    ''' Returns a decorator regarding is_superuser '''
    def decorator(view_func):
        ''' Decorator that provide the current_site and verify the
        access_right of the user '''
        @wraps(view_func, assigned=available_attrs(view_func))
        def __wrapped_view(request, *args, **kwargs):
            queryset = request.user.websites_owned

            if is_superuser is not None:
                queryset = queryset.filter(is_superuser=is_superuser)

            try:
                request.current_site = \
                    queryset.get(website__id=request.website.id).website
            except WebSiteOwner.DoesNotExist:
                request.current_site = None
                return forbidden_access()

            return view_func(request, *args, **kwargs)
        return login_required(__wrapped_view)
    return decorator

ajax_website_owner =  ajax_website_right(is_superuser=None)
ajax_website_owner_only = ajax_website_right(is_superuser=False)
ajax_website_superuser = ajax_website_right(is_superuser=True)
