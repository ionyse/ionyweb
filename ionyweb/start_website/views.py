# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.contrib.sites.models import Site, RequestSite
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext

from ionyweb.start_website.forms import StartWebsite
from ionyweb.website.decorators import admin_required
from ionyweb.website.models import WebSite, WebSiteOwner
from ionyweb.page.models import Page

from django.utils.translation import ugettext as _

def index(request):
    if WebSite.objects.count() > 0:
        # Only to set up the first website
        raise Http404

    if request.method == "POST":
        form = StartWebsite(request.POST)
        if form.is_valid():
            # 1. Create domain name
            site = Site.objects.get(pk=1)
            site.name = form.cleaned_data['name']
            site.domain = form.cleaned_data['domain']
            site.save()

            # 2. Create the website
            website = WebSite.objects.create(slug=form.cleaned_data['slug'],
                                             title=form.cleaned_data['name'],
                                             domain=site,
                                             theme=form.cleaned_data['theme'],
                                             default_layout=form.cleaned_data['layout'],)
            website.ndds.add(site)

            # 3. Create the website owner
            website_owner = WebSiteOwner.objects.create(website=website,
                                                        user=User.objects.get(pk=1),
                                                        is_superuser=True)

            # 4. Create the home page
            ct = ContentType.objects.get(app_label='page_text', model='pageapp_text')

            page = Page.objects.create(website=website,
                                       title=_(u'Home'),
                                       slug='',
                                       app_page_type=ct)

            return HttpResponseRedirect('/')
    else:
        form = StartWebsite(initial={'domain': RequestSite(request).domain})

    return render_to_response('errors/website_error.html',
                              {'form': form},
                              context_instance=RequestContext(request))
