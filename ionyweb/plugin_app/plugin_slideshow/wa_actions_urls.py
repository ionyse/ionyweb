# -*- coding: utf-8 -*-
from ionyweb.administration.actions.utils import get_actions_urls

from models import Slide
from forms import SlideForm

# Generic Action View
urlpatterns = get_actions_urls(Slide,
                               form_class=SlideForm,
                               sortable=True,
                               list_display=('image', 'get_thumb')
                               )
