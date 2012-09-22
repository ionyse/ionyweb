# -*- coding: utf-8 -*-
from django.conf import settings
from ionyweb.website.rendering.utils import render_view

def index_view(request, page_app):
    
    return render_view('page_dev_css/index.html',
                       {'object': page_app,
                        'STATIC_URL': settings.STATIC_URL})
