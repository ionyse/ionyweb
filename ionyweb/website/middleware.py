# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib.sites.models import RequestSite, Site
from django.db import DatabaseError
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext

from ionyweb.website.models import WebSite, WebSiteOwner
from ionyweb.website.views import render_website

class ProvideWebSiteMiddleware():
    def process_request(self, request):
        """
         First get the domain name of the current website :
            a : It could be a primary domain name then get the Website object
            b : It could be a secondary domain name then PermanentRedirect 
                to the primary one.
        """
        
        assert hasattr(request, 'user'), "The ProvideWebSiteMiddleware requires"
        " the AuthenticationMiddleware to be installed. Edit your"
        " MIDDLEWARE_CLASSES setting to insert"
        " 'django.contrib.auth.middleware.AuthenticationMiddleware' before it."

        
        # if settings.DEBUG:
        #     print "-"*25, "\nProvideWebSiteMiddleware()\n", "-"*25
        
        current_domain = RequestSite(request).domain
        request.website = None
        request.is_admin = False
        request.is_superuser = False

        try:
            # if settings.DEBUG:
            #     print "current_domain :", current_domain
            request.website = WebSite.objects.get(ndds__domain=current_domain)

            # if settings.DEBUG:
            #     print "REQUEST WEBSITE -----> ", request.website

            # Est-ce le domain principal
            # if settings.DEBUG:
            #     print "request.website.domain : ", request.website.domain
            if current_domain != request.website.domain.domain:
                return HttpResponsePermanentRedirect(
                    request.website.get_absolute_url())

            # Vérification des droits de l'utilisateur
            if request.user.is_authenticated():
                try:
                    owner = request.website.websites_owned.get(user=request.user)
                    request.is_admin = True
                    request.is_superuser = owner.is_superuser
                except WebSiteOwner.DoesNotExist:
                    request.is_admin = request.is_superuser = request.user.is_staff

        except WebSite.DoesNotExist:
            if not request.path.startswith('/_'):
                return HttpResponseRedirect('/_install/')
            return None
        except DatabaseError:
            return render_to_response('errors/database_error.html',
                                      context_instance=RequestContext(request))

        return None

class PreamptiveWebSiteMiddleware(object):
    def process_request(self, request):
        if not request.path_info.startswith('/_'):
            return render_website(request, request.path_info)
        else:
            return None
