# -*- coding: utf-8 -*-

from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django import VERSION as django_version

from djangorestframework.response import Response, ErrorResponse
from djangorestframework import status

from ionyweb.administration.views import IsAdminView, IsSuperAdminView
from ionyweb.administration.utils import MESSAGES
from ionyweb import VERSION_INFO as IONYWEB_VERSION
from ionyweb.website.forms import (Website_AnalyticsForm, 
                                  Website_ReferencementForm,
                                  DomainWAForm)

import sys

class Domains(IsSuperAdminView):
    
    def get(self, request):
        domains = request.website.ndds.order_by('domain')
        primary_domain = request.website.domain
        
        html = render_to_string('administration/website/domains.html',
                                {'domains': domains,
                                 'primary_domain': primary_domain},
                                context_instance = RequestContext(request))
        
        response = Response(status.HTTP_200_OK, {"html": html})
        return self.render(response)

class Domain(IsSuperAdminView):

    def get(self, request, pk=None):
        # Create the form
        if pk is None:
            form = DomainWAForm()
        else:
            site = get_object_or_404(request.website.ndds, pk=pk)
            form = DomainWAForm(instance=site)

        html = render_to_string('administration/website/domain.html',
                                {'form': form,
                                 'edit': pk is not None},
                                context_instance = RequestContext(request))

        response = Response(status.HTTP_200_OK, {"html": html})
        return self.render(response)

    def put(self, request):
        form = DomainWAForm(self.DATA)
        
        if form.is_valid():
            site = form.save()
            request.website.ndds.add(site)
            response = Response(status.HTTP_200_OK, {'msg': MESSAGES.get('item_creation_success', "")})
        else:
            html = render_to_string('administration/website/domain.html',
                                    {'form': form,
                                     'edit': False},
                                    context_instance = RequestContext(request))

            response = Response(status.HTTP_400_BAD_REQUEST,
                                {"html": html,
                                 'msg': MESSAGES.get('default_error', "")})
        return self.render(response)

    def post(self, request, pk):
        domain = get_object_or_404(request.website.ndds, pk=pk)

        if 'primary' in request.POST:
            request.website.domain = domain
            request.website.save()
            response = Response(status.HTTP_202_ACCEPTED, 
                                {'location': 'http://%s%s#admin' % 
                                 (domain.domain, request.page.get_absolute_url())})
        else:
            form = DomainWAForm(request.POST, instance=domain)

            if form.is_valid():
                form.save()
                response = Response(status.HTTP_200_OK, {'msg': MESSAGES.get('item_edit_success', "")})
            else:
                html = render_to_string('administration/website/domain.html',
                                        {'form': form,
                                         'edit': True},
                                        context_instance = RequestContext(request))
                
                response = Response(status.HTTP_400_BAD_REQUEST,
                                    {"html": html,
                                     'msg': MESSAGES.get('default_error', "")})
        return self.render(response)

    def delete(self, request, pk):
        domain = get_object_or_404(request.website.ndds, pk=pk)

        # You cannot delete the primary domain
        if request.website.domain == domain:
            response = Response(status.HTTP_400_BAD_REQUEST,
                                {'msg': MESSAGES.get('default_error', "")})
        else:
            domain.delete()
            response = Response(status.HTTP_200_OK,
                                {"msg": MESSAGES.get('item_delete_success', "")})
        # Send response
        return self.render(response)
        
class Versions(IsAdminView):
    
    def get(self, request):
        
        v_python = sys.version_info
        v_python = "%s.%s.%s" % sys.version_info[:3]
        v_django = str(django_version[0]) + "." + str(django_version[1]) + "." + str(django_version[2]) + " " + str(django_version[3])
        
        
        html = render_to_string('administration/website/versions.html',
                                {'v_python': v_python,
                                 'v_django': v_django,
                                 'v_ionyweb': IONYWEB_VERSION,},
                                context_instance = RequestContext(request))
        
        response = Response(status.HTTP_200_OK, {"html": html})
        return self.render(response)
    
class Analytics(IsSuperAdminView):
    
    def get(self, request):
        form = Website_AnalyticsForm(instance=request.website)
        
        html = render_to_string('administration/website/analytics.html',
                                {'form': form,},
                                context_instance = RequestContext(request))
        
        response = Response(status.HTTP_200_OK, {"html": html})
        return self.render(response)
    
    def post(self, request):
        
        form = Website_AnalyticsForm(request.POST, instance=request.website)
        
        if form.is_valid():
            
            form.save()
            
            response = Response(status.HTTP_200_OK, {})
            return self.render(response)
        else:
            raise ErrorResponse(status.HTTP_400_BAD_REQUEST,
                                    {'msg': MESSAGES.get('default_error', "")})
            
            
#
class Referencement(IsAdminView):
    
    def get(self, request):
        form = Website_ReferencementForm(instance=request.website)
        
        html = render_to_string('administration/website/referencement.html',
                                {'form': form,},
                                context_instance = RequestContext(request))
        
        response = Response(status.HTTP_200_OK, {"html": html})
        return self.render(response)
    
    def post(self, request):
        
        form = Website_ReferencementForm(request.POST, instance=request.website)
        
        if form.is_valid():
            
            form.save()
            
            response = Response(status.HTTP_200_OK, {})
            return self.render(response)
        else:
            raise ErrorResponse(status.HTTP_400_BAD_REQUEST,
                                    {'msg': MESSAGES.get('default_error', "")})
            
            
#
class Maintenance(IsAdminView):
    
    def get(self, request):
        html = render_to_string('administration/website/maintenance.html',
                                context_instance = RequestContext(request))
        
        response = Response(status.HTTP_200_OK, {"html": html})
        return self.render(response)
    
    def post(self, request):

        request.website.in_maintenance = not request.website.in_maintenance
        request.website.save()

        return Response(status.HTTP_202_ACCEPTED, {'location': request.page.get_absolute_url()})
            
