# -*- coding: utf-8 -*-
from django.conf import settings
from ionyweb.website.rendering.medias import JSAdminMedia
from ionyweb.website.rendering.utils import render_view

RENDER_MEDIAS = (
    JSAdminMedia('page_book_actions.js'),
    )

def index_view(request, page_app):

    return render_view('page_book/index.html', 
                       {'object': page_app,
                        'references': page_app.references,},
                       RENDER_MEDIAS,
                       is_admin_view=request.is_admin)
