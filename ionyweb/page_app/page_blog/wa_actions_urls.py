# -*- coding: utf-8 -*-
from ionyweb.administration.actions.utils import get_actions_urls
from models import Entry, Category
from forms import EntryForm, CategoryForm
from wa_actions_views import EntryActionAdminDetailView

urlpatterns = get_actions_urls(Entry, 
                               form_class=EntryForm, 
                               obj_field='blog',
                               list_display=('get_title', 'get_category', 'get_publication_date', 'get_status'),
                               detail_view_class=EntryActionAdminDetailView)

urlpatterns += get_actions_urls(Category, form_class=CategoryForm, obj_field='blog',
                                list_display=('get_title',))
