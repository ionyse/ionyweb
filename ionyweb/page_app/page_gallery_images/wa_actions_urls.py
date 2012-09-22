# -*- coding: utf-8 -*-
from ionyweb.administration.actions.utils import get_actions_urls

from models import Album, Image
from forms import AlbumForm
from actions.views import (ImageActionAdminListView,
                           ImageActionAdminDetailView)


urlpatterns = get_actions_urls(Album,
                               form_class=AlbumForm,
                               sortable=True,
                               list_display=('title', 
                                             'slug',
                                             'nb_images',
                                             'edit_images_action'))

urlpatterns += get_actions_urls(Image,
                                list_view_class=ImageActionAdminListView,
                                detail_view_class=ImageActionAdminDetailView,
                                prefix_url='album/(?P<album_pk>[0-9]*)/',
                                sortable=True,
                                list_display=('title', 
                                              'get_thumb'))
