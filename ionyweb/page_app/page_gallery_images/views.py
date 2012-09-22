# -*- coding: utf-8 -*-
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from ionyweb.website.rendering.utils import render_view
from ionyweb.website.rendering.medias import *

from models import Album

RENDER_MEDIAS = (
    # App CSS
    CSSMedia('page_gallery_images.css'),
    # Lightbox CSS
    CSSMedia('fancybox/jquery.fancybox.css', prefix_file='js'),
    # Lightbox JS
    JSMedia('fancybox/jquery.fancybox.js'),
    JSMedia('ionyweb.lightbox.js'),
    # Actions JS
    JSAdminMedia('page_gallery_images_actions.js'),
    )


def index_view(request, page_app, album_slug=None):
    """
    Display all albums of the app gallery.
    """
    context_instance=RequestContext(request)

    # Index View -- Display all albums
    if not album_slug:
        return render_view('page_gallery_images/index.html',
                           {'object': page_app},
                           RENDER_MEDIAS,
                           context_instance=context_instance)

    # Album View -- Display all images
    else:
        album = get_object_or_404(Album, slug=album_slug)
        # Displaying infos
        infos = {}
        if page_app.show_album_title:
            infos['title'] = album.title
            infos['title_rule'] = page_app.album_title_rule
        # --
        # Save object title in request
        # for plugin 'Breadcrumb'
        # --
        if settings.BREADCRUMB_PLUGIN in settings.INSTALLED_APPS:
            setattr(request, settings.BREADCRUMB_OBJECT_TITLE, album.title)
        # --
        return render_view('page_gallery_images/album.html',
                           {'object': page_app,
                            'infos': infos,
                            'album': album},
                           RENDER_MEDIAS,
                           title=album.title,
                           context_instance=context_instance)
