# -*- coding: utf-8 -*-
from ionyweb.administration.actions.utils import get_actions_urls
from models import Category, Client, Reference
from forms import ReferenceForm


urlpatterns = get_actions_urls(Category)
urlpatterns += get_actions_urls(Client)
urlpatterns += get_actions_urls(Reference, form_class=ReferenceForm, obj_field='book')
