# -*- coding: utf-8 -*-
from ionyweb.website.rendering.utils import render_view

def index_view(request, obj):
    "Render the html code in string"
    return render_view('page_text/index.html',
                       {'text': obj.text})
