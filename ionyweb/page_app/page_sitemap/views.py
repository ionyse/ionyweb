# -*- coding: utf-8 -*-
from ionyweb.website.rendering.utils import render_view

def index_view(request, page_app):
    return render_view('page_sitemap/index.html')
