# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.template import RequestContext
from ionyweb.website.rendering.utils import render_view

def index_view(request, page_app):
    if page_app.url != '':
        return HttpResponseRedirect(page_app.url)
    else:
        return render_view('page_redirect/configuration.html',
                           {'app': page_app},
                           context_instance=RequestContext(request))
